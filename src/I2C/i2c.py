"""I2C manager"""
import json
import time
from threading import Thread
from typing import Optional

from src.I2C.io.enum.button import Button
from src.I2C.io.enum.led_color import LedColor
from src.I2C.io.pcf8574.pcf8574 import Pcf8574
from src.I2C.temperature.bme280.bme_280 import BME280
from src.I2C.temperature.dto.sensor_dto import SensorDto
from src.localStorage.config import Config
from src.localStorage.jsonEncoder.file_encoder import FileEncoder
from src.network.mqtt.homeAssistant.consts import PUBLISH_DATA_SENSOR, STATE_NAME
from src.network.network import Network
from src.I2C.consts import I2C as I2C_CONST, CLASSNAME
from src.shared.enum.orders import Orders
from src.shared.logs.logs import Logs
from src.zone.consts import STATE


class I2C(Thread):
    """I2C Manager class, run a event loop for update I2C devices"""
    _instance: Optional['I2C'] = None

    def __init__(self):
        super().__init__()
        self.run_loop = True
        self.temperature_sensor = BME280()
        self.io_device = Pcf8574()
        self.temperature: Optional[SensorDto] = None
        self.zones_datas = None
        self.network = Network.get_instance()
        if Config().get_config().mqtt.enabled:
            self.network.mqtt.init_publish_i2c()
            Thread(target=self.refresh_mqtt_datas).start()

    @staticmethod
    def get_instance() -> 'I2C':
        """Return an instance of this class"""
        if not I2C._instance:
            I2C._instance = I2C()
        return I2C._instance

    def set_zones_datas(self, zones_datas):
        """Set the zones datas"""
        self.zones_datas = zones_datas

    def run(self) -> None:
        config_i2c = Config().get_config().i2c
        led1 = None
        led2 = None
        if not config_i2c.temperature.enabled \
                and not config_i2c.io.enabled \
                and not config_i2c.screen.enabled:
            return

        if config_i2c.temperature.enabled:
            self.temperature = self.temperature_sensor.get_values()

        iterations = 0
        while self.run_loop:
            if config_i2c.io.enabled and self.zones_datas is not None:
                if self.io_device.is_bp_pressed(Button.NEXT):
                    Logs.info(CLASSNAME, "BP1 pressed !")
                if self.io_device.is_bp_pressed(Button.OK):
                    Logs.info(CLASSNAME, "BP2 pressed !")
                if LedColor.order_to_color(Orders[self.zones_datas[F'zone1_{STATE}']]) != led1:
                    led1 = LedColor.order_to_color(Orders[self.zones_datas[F'zone1_{STATE}']])
                    self.io_device.set_color(1, led1)
                if LedColor.order_to_color(Orders[self.zones_datas[F'zone2_{STATE}']]) != led2:
                    led2 = LedColor.order_to_color(Orders[self.zones_datas[F'zone2_{STATE}']])
                    self.io_device.set_color(2, led2)
            if iterations == 60 and config_i2c.temperature.enabled:
                self.temperature = self.temperature_sensor.get_values()
                iterations = 0
            iterations += 1
            time.sleep(0.5)

    def refresh_mqtt_datas(self):
        """Refresh MQTT datas, send updated datas if necessary"""
        data: Optional[SensorDto] = None
        while True:
            if self.temperature is not None and data != self.temperature:
                data = self.temperature
                self.network.mqtt.publish_data(PUBLISH_DATA_SENSOR.replace(STATE_NAME, I2C_CONST),
                                               json.dumps(data, cls=FileEncoder))
            time.sleep(0.5)

    def stop(self):
        """Stop event loop"""
        self.run_loop = False
