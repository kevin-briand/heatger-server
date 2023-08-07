"""Persistence class"""
from typing import Optional

from src.localStorage.dto.persistence_dto import PersistenceDto
from src.localStorage.local_storage import LocalStorage
from src.shared.enum.mode import Mode
from src.shared.enum.state import State
from src.zone.dto.zone_persistence_dto import ZonePersistenceDto

CLASSNAME = 'Persistence'


class Persistence(LocalStorage):
    """Load/Save Heatger state in file"""
    _initialized = False
    _instance: Optional['Persistence'] = None

    def __new__(cls, *args, **kwargs) -> 'Persistence':
        if not isinstance(cls._instance, cls):
            cls._instance = super(Persistence, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if Persistence._initialized:
            return

        super().__init__('persist.json')
        try:
            self.persist = PersistenceDto(**self.read())
        except TypeError:
            self.persist = PersistenceDto([], '', '')
            self.save_in_file()
        Persistence._initialized = True

    def save_in_file(self):
        """Save persistence object to file"""
        self.write(self.persist)

    def set_state(self, zone_id: str, state: State):
        """write order in file"""
        zone = self.get_zone(zone_id)
        zone.state = state
        self.set_zone(zone)

    def set_mode(self, zone_id: str, mode: Mode):
        """write mode in file"""
        zone = self.get_zone(zone_id)
        zone.mode = mode
        self.set_zone(zone)

    def get_state(self, zone_id: str) -> State:
        """get order in file"""
        zone = self.get_zone(zone_id)
        if zone:
            return zone.state
        return State.COMFORT

    def get_mode(self, zone_id: str) -> Mode:
        """get mode in file"""
        zone = self.get_zone(zone_id)
        if zone:
            return zone.mode
        return Mode.AUTO

    def get_zone(self, zone_id: str) -> ZonePersistenceDto:
        """return the zone matching with id or a new zone if not exist"""
        for zone in self.persist.zones:
            if zone.id == zone_id:
                return zone
        return ZonePersistenceDto(zone_id, State.ECO, Mode.AUTO)

    def set_zone(self, zone_dto: ZonePersistenceDto) -> None:
        """update the zone with the given zone_dto object"""
        zones_list = []
        for zone in self.persist.zones:
            if zone != zone_dto:
                zones_list.append(zone)
        zones_list.append(zone_dto)
        self.persist.zones = zones_list
        self.save_in_file()

    def set_token(self, token: str):
        """update the api token"""
        self.persist.api_token = token
        self.save_in_file()

    def set_frostfree_end_date(self, end_date: str):
        """update the frost-free end date"""
        self.persist.frost_free = end_date
        self.save_in_file()

    def get_frostfree_end_date(self):
        """return the current frost-free end date"""
        return self.persist.frost_free

    def get_api_token(self):
        """return the api token"""
        return self.persist.api_token
