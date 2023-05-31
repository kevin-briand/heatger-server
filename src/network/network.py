from src.localStorage.config import Config
from src.network.mqtt.consts import MQTT
from src.network.mqtt.homeAssistant.homeAssistant import HomeAssistant
from src.shared.consts.consts import ENABLED


class Network:
    def __init__(self):
        self.mqtt = HomeAssistant()
        if Config().get_config().get(MQTT).get(ENABLED):
            self.mqtt.start()
