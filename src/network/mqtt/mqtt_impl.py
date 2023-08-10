"""Abstract class mqtt"""
from abc import ABCMeta

from paho.mqtt.client import MQTTMessage

from src.localStorage.config.config import Config
from src.network.mqtt.consts import REFRESH
from src.network.network import Network


class MqttImpl(metaclass=ABCMeta):
    """Abstract class used for implement the minimal functions to use mqtt client"""

    def __init__(self):
        self.force_refresh_mqtt_datas = False
        self.network = Network()

    def on_mqtt_message(self, message: MQTTMessage):
        """processing of messages received by mqtt"""
        if REFRESH in message.topic:
            self.force_refresh_mqtt_datas = True
            return
        if message.retain:
            return

    def subcribe_to_mqtt_on_message(self):
        """Subscribe a callback to the mqtt on_message"""
        self.network.mqtt.subcribe_on_message(self.on_mqtt_message)

    def refresh_mqtt_datas(self, topic: str, datas: str):
        """function to call when you want update mqtt datas"""
        if not Config().get_config().mqtt.enabled:
            return
        self.force_refresh_mqtt_datas = False
        self.network.mqtt.publish_data(topic, datas)
