"""object for config file"""
from dataclasses import dataclass


@dataclass
class MqttDto:
    """network data object"""

    # pylint: disable=unused-argument
    def __init__(self, enabled, host, port, username, password, **kwargs):
        self.enabled = enabled
        self.host = host
        self.port = port
        self.username = username
        self.password = password
