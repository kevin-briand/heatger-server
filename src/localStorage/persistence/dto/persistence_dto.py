"""object for persistence file"""
from dataclasses import dataclass
from typing import List

from src.zone.dto.zone_persistence_dto import ZonePersistenceDto


@dataclass
class PersistenceDto:
    """persistence data object"""

    # pylint: disable=unused-argument
    def __init__(self, zones: [], frost_free: str, api_token: str, **kwargs):
        self.frost_free = frost_free
        zones_list = []
        if self.is_list_of_zone_persistence_dto(zones):
            zones_list = zones
        else:
            for zone in zones:
                zones_list.append(ZonePersistenceDto(**zone))
        self.zones = zones_list
        self.api_token = api_token

    @staticmethod
    def is_list_of_zone_persistence_dto(obj: list) -> bool:
        """return true if the given list is a list of ZonePersistenceDto"""
        return isinstance(obj, List) and all(isinstance(item, ZonePersistenceDto) for item in obj)
