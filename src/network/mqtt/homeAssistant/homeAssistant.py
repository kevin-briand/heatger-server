import time

from src.I2C.temperature.consts import TEMPERATURE, CELCIUS, PERCENT, HUMIDITY, PRESSURE, HECTOPASCAL
from src.electricMeter.consts import ELECTRIC_METER
from src.localStorage.config import Config
from src.network.mqtt.homeAssistant.consts import CLASSNAME, CLASS_TEMPERATURE, \
    CLASS_HUMIDITY, CLASS_PRESSURE, CLASS_GENERIC, CLASS_DURATION, SECOND, BUTTON, BUTTON_AUTO, BUTTON_STATE, \
    BUTTON_FROSTFREE, FROSTFREE, CLASS_ENERGY, WH, TOTAL_INCREASING
from src.network.mqtt.homeAssistant.dto.publishConfig import PublishConfig
from src.network.mqtt.mqtt import Mqtt
from src.shared.logs.logs import Logs
from src.zone.consts import NAME, REMAINING_TIME, STATE, NEXT_CHANGE, MODE


class HomeAssistant(Mqtt):

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

    def on_connect(self, client, userdata, flags, rc):
        Logs.info(CLASSNAME, "Connected")

    def on_message(self, client, userdata, message):
        Logs.info(CLASSNAME, message.topic)

    def publish_data(self, url: str, data: str):
        if self.enabled:
            message_info = self.client.publish(url, data)
            try:
                message_info.wait_for_publish()
            except RuntimeError as error:
                if 'not currently connected' in repr(error):
                    time.sleep(1)
                    self.publish_data(url, data)

    def init_publish_i2c(self):
        publish_config = []
        conf_i2c = Config().get_config().i2c
        if conf_i2c.temperature.enabled:
            publish_config.append(PublishConfig(TEMPERATURE, CLASS_TEMPERATURE, CELCIUS).sensor())
            publish_config.append(PublishConfig(HUMIDITY, CLASS_HUMIDITY, PERCENT).sensor())
            publish_config.append(PublishConfig(PRESSURE, CLASS_PRESSURE, HECTOPASCAL).sensor())
        if conf_i2c.io.enabled:
            publish_config.append([PRESSURE, PublishConfig(TEMPERATURE, CELCIUS)])
        self.publish_config(publish_config)

    def init_publish_zone(self, name: str):
        Logs.info(CLASSNAME, F'publish - sensors {name}')
        config = [PublishConfig(F"{name}_{NAME}", CLASS_GENERIC).sensor(),
                  PublishConfig(F"{name}_{STATE}", CLASS_GENERIC).sensor(),
                  PublishConfig(F"{name}_{NEXT_CHANGE}", CLASS_GENERIC).sensor(),
                  PublishConfig(F"{name}_{REMAINING_TIME}", CLASS_DURATION, SECOND).sensor(),
                  PublishConfig(F"{name}_{MODE}", CLASS_GENERIC).sensor()]
        self.publish_config(config)

    def init_publish_global(self):
        Logs.info(CLASSNAME, F'publish - global sensors')
        publish_config = [PublishConfig(FROSTFREE, CLASS_DURATION, SECOND).sensor(),
                          PublishConfig(ELECTRIC_METER, CLASS_ENERGY, WH, TOTAL_INCREASING).sensor()]
        self.publish_config(publish_config)

    def init_subscribe_global(self):
        Logs.info(CLASSNAME, F'subscribe - global buttons')
        self.client.subscribe(BUTTON + BUTTON_FROSTFREE)

    def init_subscribe_zone(self, name: str):
        Logs.info(CLASSNAME, F'subscribe - buttons {name}')
        self.client.subscribe(BUTTON + BUTTON_AUTO + F'_{name}'),
        self.client.subscribe(BUTTON + BUTTON_STATE + F'_{name}')
