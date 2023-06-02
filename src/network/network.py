from src.localStorage.config import Config
from src.network.mqtt.homeAssistant.homeAssistant import HomeAssistant


class Network:
    def __init__(self):
        self.mqtt = HomeAssistant()
        if Config().get_config().mqtt.enabled:
            self.mqtt.start()
