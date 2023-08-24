"""object for config file"""
from dataclasses import dataclass


@dataclass
class DeviceDto:
    """Device data object"""

    # pylint: disable=unused-argument
    def __init__(self, address: str, port: int, **kwargs):
        self.address = int(address, 16)
        self.port = port

    def to_object(self) -> {}:
        """return an object"""
        return {
            "address": hex(self.address),
            "port": self.port
        }
