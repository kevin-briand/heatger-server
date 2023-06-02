"""object for config file"""
from dataclasses import dataclass


@dataclass
class NetworkDto:
    """network data object"""

    # pylint: disable=unused-argument
    def __init__(self, enabled, ip, *args, **kwargs):
        self.enabled = enabled
        self.ip = ip
