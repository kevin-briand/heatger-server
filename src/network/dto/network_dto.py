"""object for config file"""
from dataclasses import dataclass
from typing import List

from src.network.dto.ip_dto import IpDto


@dataclass
class NetworkDto:
    """network data object"""

    # pylint: disable=unused-argument
    def __init__(self, enabled, ip, **kwargs):
        self.enabled = enabled
        self.ip = ip if self.is_list_of_ip_dto(ip) else IpDto.array_to_ip_dto(ip)

    @staticmethod
    def is_list_of_ip_dto(obj: list) -> bool:
        """return true if the given list is a list of IpDto"""
        return isinstance(obj, List) and all(isinstance(item, IpDto) for item in obj)
