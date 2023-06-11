"""Mqtt abstract class"""
import abc
import socket
from threading import Thread

import paho.mqtt.client as mqtt

from src.network.mqtt.homeAssistant.dto.sensor_config_dto import SensorConfigDto
from src.shared.logs.logs import Logs


class Mqtt(Thread, metaclass=abc.ABCMeta):
    """Abstract class"""
    def __init__(self, host: str, port: int, username: str, password: str, classname: str):
        super().__init__()
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.classname = classname

    def is_connected(self) -> bool:
        """return true if mqtt is connected"""
        return self.client.is_connected()

    def publish_config(self, data: [SensorConfigDto]):
        """publish data list"""
        for publish_config in data:
            self.client.publish(publish_config.get('url'), publish_config.get('payload'))

    def connect(self):
        """connect to the host"""
        Logs.info(self.classname, F'Connect to {self.host}:{str(self.port)}')
        self.client.username_pw_set(self.username, password=self.password)
        for i in range(3):
            try:
                self.client.connect(self.host, self.port)
                break
            except socket.timeout:
                Logs.error(self.classname, F'Fail to connect - attempt {i+1}/3')

    def run(self) -> None:
        self.connect()
        self.client.loop_forever(retry_first_connection=True)

    def set_on_message(self, on_message):
        """override default on_message function"""
        self.client.on_message = on_message

    @abc.abstractmethod
    def on_connect(self, client, userdata, flags, rc):
        """function called when mqtt successfully connected"""
        raise NotImplementedError

    @abc.abstractmethod
    def on_message(self, client, userdata, message):
        """function called when mqtt receipt a message (default function)"""
        raise NotImplementedError

    @abc.abstractmethod
    def publish_data(self, url: str, data: str):
        """Send data to the broker"""
        raise NotImplementedError

    @abc.abstractmethod
    def init_publish_zone(self, name: str):
        """initialise zone sensors"""
        raise NotImplementedError

    @abc.abstractmethod
    def init_subscribe_zone(self, name: str):
        """initialise zone buttons"""
        raise NotImplementedError

    @abc.abstractmethod
    def init_publish_i2c(self):
        """initialise i2c sensors"""
        raise NotImplementedError
