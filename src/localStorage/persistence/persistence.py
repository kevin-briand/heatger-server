"""Persistence class"""
from datetime import datetime
from typing import Optional

from src.localStorage.persistence.dto.persistence_dto import PersistenceDto
from src.localStorage.local_storage import LocalStorage
from src.shared.enum.mode import Mode
from src.shared.enum.state import State
from src.zone.dto.zone_persistence_dto import ZonePersistenceDto


class Persistence(LocalStorage):
    """Load/Save Heatger states in file"""
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
            self.persist = PersistenceDto(**self._read())
        except TypeError:
            self.persist = PersistenceDto([], '', '')
            self.__save_in_file()
        Persistence._initialized = True

    def __save_in_file(self):
        """Save persistence object to file"""
        self._write(self.persist)

    def get_state(self, zone_id: str) -> State:
        """get order in file"""
        zone = self.__get_zone(zone_id)
        return zone.state

    def set_state(self, zone_id: str, state: State):
        """write order in file"""
        zone = self.__get_zone(zone_id)
        zone.state = state
        self.__set_zone(zone)

    def get_mode(self, zone_id: str) -> Mode:
        """get mode in file"""
        zone = self.__get_zone(zone_id)
        return zone.mode

    def set_mode(self, zone_id: str, mode: Mode):
        """write mode in file"""
        zone = self.__get_zone(zone_id)
        zone.mode = mode
        self.__set_zone(zone)

    def __get_zone(self, zone_id: str) -> ZonePersistenceDto:
        """return the zone matching with id or a new zone if not exist"""
        for zone in self.persist.zones:
            if zone.zone_id == zone_id:
                return zone
        return ZonePersistenceDto(zone_id, State.ECO, Mode.AUTO)

    def __set_zone(self, zone_dto: ZonePersistenceDto) -> None:
        """update the zone with the given zone_dto object"""
        zones_list = []
        for zone in self.persist.zones:
            if zone != zone_dto:
                zones_list.append(zone)
        zones_list.append(zone_dto)
        self.persist.zones = zones_list
        self.__save_in_file()

    def get_api_token(self) -> str:
        """return the api token"""
        return self.persist.api_token

    def set_api_token(self, token: str) -> None:
        """update the api token"""
        self.persist.api_token = token
        self.__save_in_file()

    def set_frostfree_end_date(self, end_date: datetime = None) -> None:
        """update the frost-free end date"""
        if not end_date:
            self.persist.frost_free = ''
        else:
            self.persist.frost_free = end_date.strftime('%Y-%m-%d %H:%M')
        self.__save_in_file()

    def get_frostfree_end_date(self) -> Optional[datetime]:
        """return the current frost-free end date"""
        if self.persist.frost_free == '':
            return None
        return datetime.strptime(self.persist.frost_free, '%Y-%m-%d %H:%M')
