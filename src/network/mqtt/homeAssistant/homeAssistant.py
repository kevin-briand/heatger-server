import time

from src.I2C.consts import I2C
from src.I2C.io.consts import IO
from src.I2C.temperature.consts import TEMPERATURE, CELCIUS, PERCENT, HUMIDITY, PRESSURE, HECTOPASCAL
from src.localStorage.config import Config
from src.network.mqtt import consts
from src.network.mqtt.homeAssistant.consts import CLASSNAME, CLASS_TEMPERATURE, \
    CLASS_HUMIDITY, CLASS_PRESSURE, CLASS_GENERIC, CLASS_DURATION, SECOND, BUTTON, BUTTON_AUTO, BUTTON_STATE
from src.network.mqtt.homeAssistant.dto.publishConfig import PublishConfig
from src.network.mqtt.mqtt import Mqtt
from src.shared.consts.consts import ENABLED
from src.shared.message.message import info
from src.zone.consts import NAME, REMAINING_TIME, STATE, NEXT_CHANGE, MODE


class HomeAssistant(Mqtt):

    def __init__(self):
        config = Config().get_config().get(consts.MQTT)
        self.enabled = config.get(ENABLED)
        if self.enabled:
            info(CLASSNAME, 'Init...')
            super().__init__(config.get(consts.HOST),
                             config.get(consts.PORT),
                             config.get(consts.USERNAME),
                             config.get(consts.PASSWORD),
                             CLASSNAME)

    def on_connect(self, client, userdata, flags, rc):
        info(CLASSNAME, "Connected !")

    def on_message(self, client, userdata, message):
        info(CLASSNAME, message.topic)

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
        config = Config().get_config()
        if config[I2C][TEMPERATURE][ENABLED]:
            publish_config.append(PublishConfig(TEMPERATURE, CLASS_TEMPERATURE, CELCIUS).sensor())
            publish_config.append(PublishConfig(HUMIDITY, CLASS_HUMIDITY, PERCENT).sensor())
            publish_config.append(PublishConfig(PRESSURE, CLASS_PRESSURE, HECTOPASCAL).sensor())
        if config[I2C][IO][ENABLED]:
            publish_config.append([PRESSURE, PublishConfig(TEMPERATURE, CELCIUS)])
        self.publish_config(publish_config)

    def init_publish_zone(self, name: str):
        config = [PublishConfig(F"{name}_{NAME}", CLASS_GENERIC).sensor(),
                  PublishConfig(F"{name}_{STATE}", CLASS_GENERIC).sensor(),
                  PublishConfig(F"{name}_{NEXT_CHANGE}", CLASS_GENERIC).sensor(),
                  PublishConfig(F"{name}_{REMAINING_TIME}", CLASS_DURATION, SECOND).sensor(),
                  PublishConfig(F"{name}_{MODE}", CLASS_GENERIC).sensor()]
        self.publish_config(config)

    def init_subscribe_zone(self, name: str):
        info(CLASSNAME, F'subscribe - buttons {name}')
        self.client.subscribe(BUTTON + BUTTON_AUTO + F'_{name}'),
        self.client.subscribe(BUTTON + BUTTON_STATE + F'_{name}')
