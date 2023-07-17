"""Network class"""
from typing import Optional

from src.localStorage.config import Config
from src.network.mqtt.homeAssistant.consts import CLASSNAME
from src.network.mqtt.homeAssistant.home_assistant import HomeAssistant
from src.shared.logs.logs import Logs


class Network:
    """Class for initialise network(mqtt)"""
    _instance: Optional['Network'] = None

    def __init__(self):
        self.mqtt = HomeAssistant()
        if Config().get_config().mqtt.enabled:
            self.mqtt.start()
            Logs.info(CLASSNAME, "Started !")

    @staticmethod
    def get_instance() -> 'Network':
        """Return an instance of this class"""
        if not Network._instance:
            Network._instance = Network()
        return Network._instance
