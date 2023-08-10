"""object for config file"""
from dataclasses import dataclass
from typing import List


@dataclass
class IpDto:
    """Ip data object"""

    # pylint: disable=unused-argument
    def __init__(self, name, ip, **kwargs):
        self.name = name
        self.ip = ip

    def __eq__(self, other: 'IpDto'):
        if other is None:
            return False
        return self.ip == other.ip

    @staticmethod
    def array_to_ip_dto(data: []) -> List['IpDto']:
        """convert json array to array of IpDto"""
        list_ip = []
        for ip in data:
            list_ip.append(IpDto(ip['name'], ip['ip']))
        return list_ip

    @staticmethod
    def object_to_ip_dto(data: {}) -> 'IpDto':
        """convert json object to IpDto"""
        return IpDto(data['name'], data['ip'])
