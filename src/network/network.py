"""Network class"""
from src.localStorage.config import Config
from src.network.mqtt.homeAssistant.home_assistant import HomeAssistant


class Network:
    """Class for initialise network(mqtt)"""
    def __init__(self):
        self.mqtt = HomeAssistant()
        if Config().get_config().mqtt.enabled:
            self.mqtt.start()
