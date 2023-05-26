import time

from src.I2C.consts import I2C
from src.I2C.io.consts import IO
from src.I2C.temperature.consts import TEMPERATURE, CELCIUS, PERCENT, HUMIDITY, PRESSURE, HECTOPASCAL
from src.localStorage.config import Config
from src.network.mqtt import consts
from src.network.mqtt.homeAssistant.consts import CLASSNAME, CLASS_TEMPERATURE, \
    CLASS_HUMIDITY, CLASS_PRESSURE, CLASS_GENERIC, CLASS_DURATION, SECOND
from src.network.mqtt.homeAssistant.dto.publishConfig import PublishConfig
from src.network.mqtt.mqtt import Mqtt
from src.shared.consts.consts import ENABLED
from src.shared.message.message import info
from src.zone.consts import ZONE, NAME, REMAINING_TIME, STATE, NEXT_CHANGE


class HomeAssistant(Mqtt):

    def __init__(self):
        config = Config().get_config().get(consts.MQTT)
        super().__init__(config.get(consts.HOST),
                         config.get(consts.PORT),
                         config.get(consts.USERNAME),
                         config.get(consts.PASSWORD))

    def run(self) -> None:
        self.connect()
        # self.client.subscribe('home/domoserv/tempInt')
        self.client.loop_forever(retry_first_connection=True)

    def on_connect(self, client, userdata, flags, rc):
        info(CLASSNAME, "Connected !")
        self.publish_config(self.init_publish())

    def publish_data(self, url: str, data: str):
        message_info = self.client.publish(url, data)
        try:
            message_info.wait_for_publish()
        except RuntimeError as error:
            if 'not currently connected' in repr(error):
                time.sleep(1)
                self.publish_data(url, data)

    def publish_config(self, data):
        for publish_config in data:
            info(CLASSNAME, F'publish - {publish_config.get("name")}')
            self.client.publish(publish_config["url"], publish_config.get('payload'))

    @staticmethod
    def init_publish() -> []:
        publish_config = []
        config = Config().get_config()
        i = 1
        while config.get(F"{ZONE}{i}") is not None:
            publish_config.append(PublishConfig(F"{ZONE}{i}_{NAME}", CLASS_GENERIC).sensor())
            publish_config.append(PublishConfig(F"{ZONE}{i}_{STATE}", CLASS_GENERIC).sensor())
            publish_config.append(PublishConfig(F"{ZONE}{i}_{NEXT_CHANGE}", CLASS_GENERIC).sensor())
            publish_config.append(PublishConfig(F"{ZONE}{i}_{REMAINING_TIME}", CLASS_DURATION, SECOND).sensor())
            i = i + 1

        if config[I2C][TEMPERATURE][ENABLED]:
            publish_config.append(PublishConfig(TEMPERATURE, CLASS_TEMPERATURE, CELCIUS).sensor())
            publish_config.append(PublishConfig(HUMIDITY, CLASS_HUMIDITY, PERCENT).sensor())
            publish_config.append(PublishConfig(PRESSURE, CLASS_PRESSURE, HECTOPASCAL).sensor())
        if config[I2C][IO][ENABLED]:
            publish_config.append([PRESSURE, PublishConfig(TEMPERATURE, CELCIUS)])
        return publish_config
