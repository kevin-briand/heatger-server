"""object for persistence file"""
from dataclasses import dataclass

from src.zone.dto.zone_persistence_dto import ZonePersistenceDto


@dataclass
class PersistenceDto:
    """persistence data object"""

    # pylint: disable=unused-argument
    def __init__(self, zones: [], frost_free: str, api_token: str, **kwargs):
        self.frost_free = frost_free
        zones_list = []
        for zone in zones:
            zones_list.append(ZonePersistenceDto(**zone))
        self.zones = zones_list
        self.api_token = api_token
