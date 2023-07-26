"""Abstract class mqtt"""
from abc import ABCMeta
from typing import Any

from src.localStorage.config import Config
from src.network.mqtt.consts import REFRESH
from src.network.network import Network


class MqttImpl(metaclass=ABCMeta):
    """Abstract class used for implement the minimal functions to use mqtt client"""
    def __init__(self):
        self.force_refresh_mqtt_datas = False
        self.network = Network()
        self.network.mqtt.subcribe_on_message(self.on_mqtt_message)

    def on_mqtt_message(self, message: Any):
        """processing of messages received by mqtt"""
        if REFRESH in message:
            self.force_refresh_mqtt_datas = True
            return
        if message.retain:
            return

    def refresh_mqtt_datas(self, topic: str, datas: str):
        """function to call when you want update mqtt datas"""
        if Config().get_config().mqtt.enabled:
            self.force_refresh_mqtt_datas = False
            self.network.mqtt.publish_data(topic, datas)
