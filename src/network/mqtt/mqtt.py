import abc
from threading import Thread

import paho.mqtt.client as mqtt

from src.shared.message.message import info

CLASSNAME = 'MQTT'


def on_connect(client, userdata, flags, rc):
    print("Mqtt: " + mqtt.connack_string(rc))


def on_message(client, userdata, message):
    info(CLASSNAME, message.payload)


class Mqtt(Thread, metaclass=abc.ABCMeta):
    def __init__(self, host: str, port: int, username: str, password: str):
        super().__init__()
        info(CLASSNAME, 'Init...')
        self.client = mqtt.Client()
        self.client.on_connect = on_connect
        self.client.on_message = on_message
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    @abc.abstractmethod
    def run(self) -> None:
        raise NotImplementedError

    def connect(self):
        info(CLASSNAME, F'Connect to {self.host}:{str(self.port)}')
        self.client.username_pw_set(self.username, password=self.password)
        self.client.connect(self.host, self.port)
