"""object for config file"""
from dataclasses import dataclass

from src.network.dto.ip_dto import IpDto


@dataclass
class NetworkDto:
    """network data object"""

    # pylint: disable=unused-argument
    def __init__(self, enabled, ip, *args, **kwargs):
        self.enabled = enabled
        self.ip = IpDto.array_to_ip_dto(ip)
