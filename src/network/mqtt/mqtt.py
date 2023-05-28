import abc
from threading import Thread

import paho.mqtt.client as mqtt
from src.shared.message.message import info


class Mqtt(Thread, metaclass=abc.ABCMeta):
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

    def is_connected(self):
        return self.client.is_connected()

    def publish_config(self, data):
        for publish_config in data:
            info(self.classname, F'publish - {publish_config.get("name")}')
            self.client.publish(publish_config["url"], publish_config.get('payload'))

    def connect(self):
        info(self.classname, F'Connect to {self.host}:{str(self.port)}')
        self.client.username_pw_set(self.username, password=self.password)
        self.client.connect(self.host, self.port)

    def run(self) -> None:
        self.connect()
        self.client.loop_forever(retry_first_connection=True)

    def set_on_message(self, on_message):
        self.client.on_message = on_message

    @abc.abstractmethod
    def on_connect(self, client, userdata, flags, rc):
        raise NotImplementedError
    @abc.abstractmethod
    def on_message(self, client, userdata, message):
        raise NotImplementedError

    @abc.abstractmethod
    def publish_data(self, url: str, data: str):
        raise NotImplementedError

    @abc.abstractmethod
    def init_publish_zone(self, name: str):
        raise NotImplementedError

    @abc.abstractmethod
    def init_subscribe_zone(self, name: str):
        raise NotImplementedError

    @abc.abstractmethod
    def init_publish_i2c(self):
        raise NotImplementedError
