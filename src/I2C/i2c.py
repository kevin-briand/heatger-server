"""I2C manager"""
import json
import time
from threading import Thread
from typing import Optional, Callable

from src.I2C.io.enum.button import Button
from src.I2C.io.enum.led_color import LedColor
from src.I2C.io.pcf8574.pcf8574 import Pcf8574
from src.I2C.screen.dto.zone_screen_dto import ZoneScreenDto
from src.I2C.screen.enum.vue import Vue
from src.I2C.screen.screen import Screen
from src.I2C.temperature.bme280.bme_280 import BME280
from src.I2C.temperature.dto.sensor_dto import SensorDto
from src.localStorage.config import Config
from src.localStorage.jsonEncoder.file_encoder import FileEncoder
from src.network.mqtt.homeAssistant.consts import PUBLISH_DATA_SENSOR, STATE_NAME
from src.network.mqtt.mqtt_impl import MqttImpl
from src.network.network import Network
from src.I2C.consts import I2C as I2C_CONST, CLASSNAME, ZONE1, ZONE2
from src.shared.enum.state import State
from src.shared.logs.logs import Logs
from src.zone.consts import STATE


class I2C(Thread, MqttImpl):
    """I2C Manager class, run a event loop for update I2C devices"""
    _instance: Optional['I2C'] = None
    _initialized = False

    def __new__(cls, *args, **kwargs) -> 'I2C':
        if not isinstance(cls._instance, cls):
            cls._instance = super(I2C, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        super().__init__()
        MqttImpl.__init__(self)
        self.run_loop = True
        self.temperature_sensor = BME280()
        self.io_device = Pcf8574()
        self.temperature: Optional[SensorDto] = None
        self.zones_datas = None
        self.network = Network()
        self.screen_device = Screen()
        self.screen_need_update = False
        self.toggle_order: Optional[Callable[[int], None]] = None
        self.loop_iterations = 0
        self.led1_state = None
        self.led2_state = None
        self.start()
        self.init_mqtt_data_update_loop_if_enabled()
        self._initialized = True

    def init_mqtt_data_update_loop_if_enabled(self):
        if not Config().get_config().mqtt.enabled:
            return
        self.network.mqtt.init_publish_i2c()
        Thread(target=self.refresh_mqtt_i2c_datas).start()
        self.subcribe_to_mqtt_on_message()

    def refresh_mqtt_i2c_datas(self) -> None:
        """Refresh MQTT datas, send updated datas if necessary"""
        data: Optional[SensorDto] = None
        while True:
            if self.temperature is not None and data != self.temperature or self.force_refresh_mqtt_datas:
                data = self.temperature
                self.screen_device.set_temperature(data)
                self.screen_need_update = True
                self.refresh_mqtt_datas(PUBLISH_DATA_SENSOR.replace(STATE_NAME, I2C_CONST),
                                        json.dumps(data, cls=FileEncoder))
            time.sleep(0.5)

    def set_zones_datas_and_update_screen(self, zones_datas) -> None:
        """Set the zones datas"""
        self.zones_datas = zones_datas
        self.screen_device.set_zone_info(ZoneScreenDto(State[zones_datas['zone1_state']],
                                                       State[zones_datas['zone2_state']],
                                                       zones_datas['zone1_name'],
                                                       zones_datas['zone2_name']))
        self.screen_need_update = True

    def run(self) -> None:
        if self.is_all_i2c_devices_disabled():
            return
        Logs.info(CLASSNAME, "loop started")

        config_i2c = Config().get_config().i2c
        if config_i2c.temperature.enabled:
            self.update_temperature()

        while self.run_loop:
            self.check_io_status()
            if self.loop_iterations == 60 and config_i2c.temperature.enabled:
                self.update_temperature()
            self.update_screen_if_needed()
            self.loop_iterations += 1
            time.sleep(0.1)

    @staticmethod
    def is_all_i2c_devices_disabled() -> bool:
        """Return true if all i2c devices are disabled"""
        config_i2c = Config().get_config().i2c
        if not config_i2c.temperature.enabled \
                and not config_i2c.io.enabled \
                and not config_i2c.screen.enabled:
            return True
        return False

    def update_temperature(self) -> None:
        """get the temperature datas to the sensor"""
        self.temperature = self.temperature_sensor.get_values()
        self.reset_loop_iterations()

    def check_io_status(self) -> None:
        """Check io status and perform an action if changed"""
        if not Config().get_config().i2c.io.enabled or self.zones_datas is None:
            return

        self.check_buttons_status()

        zone1_led_color = LedColor.order_to_color(State[self.zones_datas[F'zone1_{STATE}']])
        zone2_led_color = LedColor.order_to_color(State[self.zones_datas[F'zone2_{STATE}']])
        if zone1_led_color != self.led1_state:
            self.io_device.set_color(1, zone1_led_color)
        if zone2_led_color != self.led2_state:
            self.io_device.set_color(2, zone2_led_color)

    def check_buttons_status(self) -> None:
        """Check if a button is pressed. If so, perform an action."""
        if self.io_device.is_button_pressed(Button.NEXT):
            self.show_next_vue()
        if self.io_device.is_button_pressed(Button.OK):
            self.update_zone_state_if_needed()

    def show_next_vue(self) -> None:
        """update the screen with the next vue and reset the loop_iteration"""
        self.screen_device.show_next_vue()
        self.reset_loop_iterations()

    def update_zone_state_if_needed(self) -> None:
        """toggle order of the zone selected(if vue is SET_STATE_ZONE(x))"""
        if self.screen_device.get_current_vue() == Vue.SET_STATE_ZONE1:
            self.toggle_state_zone(ZONE1)
        if self.screen_device.get_current_vue() == Vue.SET_STATE_ZONE2:
            self.toggle_state_zone(ZONE2)

    def toggle_state_zone(self, zone_number: int) -> None:
        """toggle state of the zone according to zone_number"""
        if self.toggle_order is not None:
            self.toggle_order(zone_number)
        self.reset_loop_iterations()

    def update_screen_if_needed(self) -> None:
        """update screen vue if screen_need_update is True"""
        if self.screen_need_update and Config().get_config().i2c.screen.enabled:
            self.screen_device.draw_vue_if_vars_is_not_none()
            self.screen_need_update = False
        if self.screen_device.get_current_vue() != Vue.GENERAL and self.loop_iterations == 59:
            self.screen_device.show_general_vue()

    def stop(self) -> None:
        """Stop event loop"""
        self.run_loop = False

    def reset_loop_iterations(self) -> None:
        """Used to reset the loop_iteration variable"""
        self.loop_iterations = 0
