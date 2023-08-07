"""HomeAssistant class"""
import time

from src.I2C.consts import I2C
from src.I2C.temperature.consts import TEMPERATURE, CELCIUS, PERCENT, HUMIDITY,\
    PRESSURE, HECTOPASCAL
from src.electricMeter.consts import ELECTRIC_METER
from src.localStorage.config import Config
from src.network.mqtt.homeAssistant.consts import CLASSNAME, CLASS_TEMPERATURE, \
    CLASS_HUMIDITY, CLASS_PRESSURE, CLASS_GENERIC, BUTTON, \
    BUTTON_FROSTFREE, FROSTFREE, CLASS_ENERGY, WH, TOTAL_INCREASING, SWITCH_MODE, \
    SWITCH_STATE
from src.network.mqtt.homeAssistant.dto.button_config_dto import ButtonConfigDto
from src.network.mqtt.homeAssistant.dto.sensor_config_dto import SensorConfigDto
from src.network.mqtt.mqtt import Mqtt
from src.shared.logs.logs import Logs
from src.zone.consts import NAME, STATE, NEXT_CHANGE, MODE, IS_PING, ZONE


class HomeAssistant(Mqtt):
    """Class for communicate with home assistant(mqtt)\n
     - create new sensor
     - publish/subscribe sensors/buttons
    """
    def __init__(self):
        mqtt_conf = Config().get_config().mqtt
        self.enabled = mqtt_conf.enabled
        if self.enabled:
            Logs.info(CLASSNAME, 'Init...')
            super().__init__(mqtt_conf.host,
                             mqtt_conf.port,
                             mqtt_conf.username,
                             mqtt_conf.password,
                             CLASSNAME)

    # pylint: disable=unused-argument
    def on_connect(self, client, userdata, flags, rc):
        """function called when mqtt successfully connected"""
        Logs.info(CLASSNAME, "Connected")

    def publish_data(self, url: str, data: str):
        """Send data to the broker"""
        if self.enabled:
            message_info = self.client.publish(url, data)
            try:
                message_info.wait_for_publish()
            except RuntimeError as error:
                if 'not currently connected' in repr(error):
                    time.sleep(1)
                    self.publish_data(url, data)

    def init_publish_i2c(self):
        """initialise i2c sensors"""
        self.wait_for_connect()
        publish_conf = []
        conf_i2c = Config().get_config().i2c
        if conf_i2c.temperature.enabled:
            publish_conf.append(SensorConfigDto(TEMPERATURE,
                                                CLASS_TEMPERATURE, I2C, CELCIUS).to_object())
            publish_conf.append(SensorConfigDto(HUMIDITY, CLASS_HUMIDITY, I2C, PERCENT).to_object())
            publish_conf.append(SensorConfigDto(PRESSURE, CLASS_PRESSURE, I2C, HECTOPASCAL).to_object())
        if conf_i2c.io.enabled:
            pass
        self.publish_config(publish_conf)

    def init_publish_zone(self, name: str):
        """initialise zone sensors/buttons"""
        self.wait_for_connect()
        Logs.info(CLASSNAME, F'publish - sensors {name}')
        config = [
            SensorConfigDto(F"{name}_{NAME}", CLASS_GENERIC, state_topic_name=ZONE).to_object(),
            SensorConfigDto(F"{name}_{STATE}", CLASS_GENERIC, state_topic_name=ZONE).to_object(),
            SensorConfigDto(F"{name}_{NEXT_CHANGE}", CLASS_GENERIC, state_topic_name=ZONE).to_object(),
            SensorConfigDto(F"{name}_{IS_PING}", CLASS_GENERIC, state_topic_name=ZONE).to_object(),
            SensorConfigDto(F"{name}_{MODE}", CLASS_GENERIC, state_topic_name=ZONE).to_object(),
            ButtonConfigDto(F"{name}_{SWITCH_MODE}").to_object(),
            ButtonConfigDto(F"{name}_{SWITCH_STATE}").to_object()
        ]
        self.publish_config(config)

    def init_publish_frostfree(self):
        """initialise frostfree sensors"""
        self.wait_for_connect()
        Logs.info(CLASSNAME, 'publish - frostfree sensors')
        publish_config = [
            SensorConfigDto(FROSTFREE, CLASS_GENERIC, state_topic_name=ZONE).to_object(),
            ButtonConfigDto(FROSTFREE).to_object()
        ]
        self.publish_config(publish_config)

    def init_subscribe_frostfree(self):
        """initialise frostfree button"""
        self.wait_for_connect()
        Logs.info(CLASSNAME, 'subscribe - frostfree button')
        self.client.subscribe(BUTTON + BUTTON_FROSTFREE + '/commands')

    def init_subscribe_zone(self, name: str):
        """initialise zone buttons"""
        self.wait_for_connect()
        Logs.info(CLASSNAME, F'subscribe - buttons {name}')
        self.client.subscribe(BUTTON + F'{name}_' + SWITCH_MODE + '/commands')
        self.client.subscribe(BUTTON + F'{name}_' + SWITCH_STATE + '/commands')

    def init_publish_electric_meter(self):
        """initialise electric meter sensor"""
        self.wait_for_connect()
        Logs.info(CLASSNAME, 'publish - electric meter sensor')
        self.publish_config([
            SensorConfigDto(ELECTRIC_METER, CLASS_ENERGY, ELECTRIC_METER, WH, TOTAL_INCREASING).to_object()
        ])

    def wait_for_connect(self):
        """Wait loop, end when mqtt client is connected"""
        while not self.is_connected():
            time.sleep(0.1)
