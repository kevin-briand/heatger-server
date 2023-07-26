"""Network class"""
from typing import Optional

from src.localStorage.config import Config
from src.network.mqtt.homeAssistant.consts import CLASSNAME
from src.network.mqtt.homeAssistant.home_assistant import HomeAssistant
from src.shared.logs.logs import Logs


class Network:
    """Class for initialise network(mqtt)"""
    _instance: Optional['Network'] = None
    _initialized = False

    def __init__(self):
        if Network._initialized:
            return

        self.mqtt = HomeAssistant()
        if Config().get_config().mqtt.enabled:
            self.mqtt.start()
            Logs.info(CLASSNAME, "Started !")
        Network._initialized = True

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = super(Network, cls).__new__(cls, *args, **kwargs)
        return cls._instance
