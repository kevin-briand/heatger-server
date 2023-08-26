"""Zone manager class"""
import json
import time
from datetime import datetime
from threading import Thread
from typing import Optional

from paho.mqtt.client import MQTTMessage

from src.i2c.i2c import I2C
from src.localStorage.config.config import Config
from src.localStorage.jsonEncoder.json_encoder import JsonEncoder
from src.network.mqtt.homeAssistant.consts import SWITCH_MODE, SWITCH_STATE, \
    BUTTON_FROSTFREE, PUBLISH_DATA_SENSOR, STATE_NAME
from src.network.mqtt.mqtt_impl import MqttImpl
from src.network.network import Network
from src.shared.enum.state import State
from src.shared.logs.logs import Logs
from src.shared.timer.timer import Timer
from src.zone.consts import ZONE, CLASSNAME
from src.zone.frostfree import Frostfree
from src.zone.zone import Zone


class ZoneManager(Thread, MqttImpl):
    """This class is used for manage heaters zones"""

    def __init__(self):
        super().__init__()
        MqttImpl.__init__(self)
        self.zones: list[Zone] = []
        self.frostfree: Optional[Frostfree] = None
        self.current_datas = {}
        self.network = Network()
        self.update_datas_timer = Timer()
        self.mqtt_loop: Optional[Thread] = None
        self.mqtt_stop_loop = False
        I2C().toggle_order = self.toggle_state

    def run(self) -> None:
        self.init_zones()
        self.init_frostfree()
        self.init_mqtt_if_enabled()

    def init_zones(self) -> None:
        """zones initializer"""
        self.zones.clear()
        try:
            self.init_zones_from_config_file()
        except AttributeError:
            pass

    def init_zones_from_config_file(self) -> None:
        """Initialize zones from config file"""
        i = 1
        while getattr(Config().get_config(), F"{ZONE}{i}") is not None:
            Logs.info(F"{ZONE}{i}", F"Init Zone {i}")
            self.zones.append(Zone(i))
            i += 1

    def init_frostfree(self) -> None:
        """Frost-free initializer"""
        self.frostfree = Frostfree(self.zones)

    def init_mqtt_if_enabled(self) -> None:
        """initialize mqtt sensors/buttons"""
        if Config().get_config().mqtt.enabled:
            for i in range(1, len(self.zones)+1):
                self.network.mqtt.init_publish_zone(F"{ZONE}{i}")
                self.network.mqtt.init_subscribe_zone(F"{ZONE}{i}")
            self.network.mqtt.init_subscribe_frostfree()
            self.network.mqtt.init_publish_frostfree()
            self.mqtt_loop = Thread(target=self.refresh_datas_loop)
            self.mqtt_loop.start()
            self.subcribe_to_mqtt_on_message()

    def on_mqtt_message(self, message: MQTTMessage) -> None:
        """processing of messages received by mqtt"""
        super().on_mqtt_message(message)
        if ZONE in message.topic:
            self.processing_zone_mqtt_message(message.topic)
        elif BUTTON_FROSTFREE in message.topic:
            self.processing_frost_free_mqtt_message(message.payload.decode('utf-8'))

    def processing_zone_mqtt_message(self, message: str) -> None:
        """processing zone mqtt message"""
        number_zone = Zone.get_zone_number(message)
        if number_zone == -1:
            return
        if F'_{SWITCH_MODE}' in message:
            self.zones[number_zone - 1].toggle_mode()
        elif F'_{SWITCH_STATE}' in message:
            self.toggle_state(number_zone)

    def processing_frost_free_mqtt_message(self, payload: str) -> None:
        """processing frost-free mqtt message"""
        if payload == '':
            Logs.error(CLASSNAME, F'{State.FROSTFREE} - empty data')
            return
        try:
            end_date = datetime.strptime(payload, '%Y-%m-%dT%H:%M')
        except ValueError:
            Logs.error(CLASSNAME, F'{State.FROSTFREE} - invalid date format')
            return
        if end_date > datetime.now():
            self.frostfree.start(end_date)
        else:
            self.frostfree.stop()

    def toggle_state(self, zone_number: int) -> None:
        """switch heater state comfort<>eco"""
        self.zones[zone_number - 1].toggle_state()

    def refresh_datas_loop(self) -> None:
        """test if datas changed, if true, send new datas to MQTT and I2C class"""
        while not self.mqtt_stop_loop:
            data = {}
            for zone in self.zones:
                data.update(zone.get_data().to_object())
            data.update(self.frostfree.get_data().to_object())
            if len(self.zones) >= 2 and (data != self.current_datas or self.force_refresh_mqtt_datas):
                self.current_datas = data
                self.refresh_mqtt_zones_datas()
                self.refresh_i2c_datas()
            time.sleep(0.5)

    def refresh_mqtt_zones_datas(self) -> None:
        """Refresh MQTT datas"""
        self.refresh_mqtt_datas(PUBLISH_DATA_SENSOR.replace(STATE_NAME, ZONE),
                                json.dumps(self.current_datas, cls=JsonEncoder))

    def refresh_i2c_datas(self) -> None:
        """Refresh I2C datas"""
        I2C().set_zones_datas_and_update_screen(self.current_datas)

    def stop_loop(self):
        self.mqtt_stop_loop = True
        for zone in self.zones:
            zone.stop_loop()
        self.frostfree.stop_loop()
