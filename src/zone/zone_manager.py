"""Zone manager class"""
import json
import time
from datetime import datetime
from threading import Thread
from typing import Optional

from src.I2C.i2c import I2C
from src.localStorage.config import Config
from src.localStorage.jsonEncoder.file_encoder import FileEncoder
from src.network.mqtt.homeAssistant.consts import SWITCH_MODE, SWITCH_STATE, \
    BUTTON_FROSTFREE, PUBLISH_DATA_SENSOR, STATE_NAME
from src.network.network import Network
from src.shared.enum.orders import Orders
from src.shared.logs.logs import Logs
from src.shared.timer.timer import Timer
from src.zone.consts import ZONE, CLASSNAME
from src.zone.frostfree import Frostfree
from src.zone.zone import Zone


class ZoneManager(Thread):
    """This class is used for manage heaters zones"""
    def __init__(self):
        super().__init__()
        self.zones: list[Zone] = []
        self.frostfree: Optional[Frostfree] = None
        self.current_datas = {}
        self.network = Network.get_instance()
        self.update_datas_timer = Timer()

    def init_zones(self):
        """zones initializer"""
        self.zones.clear()
        i = 1
        mqtt_enabled = Config().get_config().mqtt.enabled
        try:
            while getattr(Config().get_config(), F"{ZONE}{i}") is not None:
                self.zones.append(Zone(i, self.network))
                if mqtt_enabled:
                    while not self.network.mqtt.is_connected():
                        continue
                    self.network.mqtt.init_publish_zone(F"{ZONE}{i}")
                    self.network.mqtt.init_subscribe_zone(F"{ZONE}{i}")
                i = i + 1
        except AttributeError:
            pass

    def init_frostfree(self):
        """Frost-free initializer"""
        self.frostfree = Frostfree(self.zones)

    def run(self) -> None:
        self.init_zones()
        self.init_frostfree()
        mqtt_enabled = Config().get_config().mqtt.enabled
        self.frostfree.restore()
        if mqtt_enabled:
            self.network.mqtt.init_subscribe_frostfree()
            self.network.mqtt.init_publish_frostfree()
            self.network.mqtt.subcribe_on_message(self.on_mqtt_message)
            Thread(target=self.refresh_datas_loop).start()

    def on_mqtt_message(self, message):
        """processing of messages received by mqtt"""
        if message.retain:
            return
        if ZONE in message.topic:
            number_zone = Zone.get_zone_number(message.topic)
            if number_zone == -1:
                return
            if F'_{SWITCH_MODE}' in message.topic:
                self.zones[number_zone].toggle_mode()
            elif F'_{SWITCH_STATE}' in message.topic:
                self.zones[number_zone].toggle_order()
        elif BUTTON_FROSTFREE in message.topic:
            payload = message.payload.decode('utf-8')
            if payload == '':
                Logs.error(CLASSNAME, F'{Orders.FROSTFREE} - empty data')
                return
            end_date = datetime.strptime(payload, '%Y-%m-%dT%H:%M')
            if end_date is None:
                Logs.error(CLASSNAME, F'{Orders.FROSTFREE} - invalid date format')
                return
            if end_date > datetime.now():
                self.frostfree.start(end_date)
            else:
                self.frostfree.stop()

    def refresh_mqtt_datas(self):
        """Refresh MQTT datas"""
        if Config().get_config().mqtt.enabled:
            self.network.mqtt.publish_data(PUBLISH_DATA_SENSOR.replace(STATE_NAME, ZONE),
                                           json.dumps(self.current_datas, cls=FileEncoder))

    def refresh_datas_loop(self):
        """test if datas changed, if true, send new datas to MQTT and I2C class"""
        while True:
            data = {}
            for zone in self.zones:
                data.update(zone.get_data().to_object())
            data.update(self.frostfree.get_data().to_object())
            if data != self.current_datas:
                self.current_datas = data
                self.refresh_mqtt_datas()
                self.refresh_i2c_datas()
            time.sleep(0.5)

    def refresh_i2c_datas(self):
        """Refresh I2C datas"""
        I2C.get_instance().set_zones_datas(self.current_datas)
