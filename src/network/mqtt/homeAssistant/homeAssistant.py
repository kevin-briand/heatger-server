from src.I2C.consts import I2C, ENABLED
from src.I2C.io.consts import IO
from src.I2C.temperature.consts import TEMPERATURE, CELCIUS, PERCENT, HUMIDITY, PRESSURE, HECTOPASCAL
from src.localStorage.config import Config
from src.network.mqtt import consts
from src.network.mqtt.homeAssistant.consts import CLASSNAME, SENSOR, CLASS_TEMPERATURE, DEVICE_MANUFACTURER, DEVICE_NAME
from src.network.mqtt.homeAssistant.dto.publishConfig import PublishConfig
from src.network.mqtt.mqtt import Mqtt
from src.shared.message.message import info


class HomeAssistant(Mqtt):

    def __init__(self):
        config = Config().get_config()[consts.MQTT]
        super().__init__(config[consts.HOST],
                         config[consts.PORT],
                         config[consts.USERNAME],
                         config[consts.PASSWORD])

    @staticmethod
    def sensor_payload(self, name: str, unit_of_measurement=''):
        return {
            "name": name,
            "unique_id": name,
            "unit_of_measurement": unit_of_measurement,
            "value_template": "{{ value_json." + name + " }}",
            "device_class": CLASS_TEMPERATURE,
            "state_topic": SENSOR + "heatger/state",
            "device": {
                "identifiers": ["heatger"],
                "manufacturer": DEVICE_MANUFACTURER,
                "name": DEVICE_NAME
            }
        }

    def run(self) -> None:
        self.connect()
        self.publish_config(self.init_publish())
        # self.publish_data(SENSOR + 'heatger/state', '{"temperature": "21", "humidity": "62"}')
        # self.client.subscribe('home/domoserv/tempInt')
        self.client.loop_forever(retry_first_connection=True)

    def publish_config(self, data):
        for publish_config in data:
            info(CLASSNAME, F'publish - {publish_config["name"]}')
            self.client.publish(publish_config["url"], publish_config['payload'])

    def init_publish(self) -> []:
        publish_config = []
        config = Config().get_config()
        if config[I2C][TEMPERATURE][ENABLED]:
            publish_config.append(PublishConfig(TEMPERATURE, CELCIUS).sensor())
            publish_config.append(PublishConfig(HUMIDITY, PERCENT).sensor())
            publish_config.append(PublishConfig(PRESSURE, HECTOPASCAL).sensor())
        if config[I2C][IO][ENABLED]:
            publish_config[publish_config+1] = [PRESSURE, PublishConfig(TEMPERATURE, CELCIUS)]
        return publish_config
