"""Config class"""
from typing import Optional

from src.localStorage.config.dto.config_dto import ConfigDto
from src.localStorage.config.errors.zone_not_found_error import ZoneNotFoundError
from src.localStorage.errors.missing_arg_error import MissingArgError
from src.localStorage.local_storage import LocalStorage
from src.zone.dto.zone_dto import ZoneDto


class Config(LocalStorage):
    """Class for reading/writing the configuration in file"""
    _initialized = False
    _instance: Optional['Config'] = None

    def __new__(cls, *args, **kwargs) -> 'Config':
        if not isinstance(cls._instance, cls):
            cls._instance = super(Config, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if Config._initialized:
            return
        super().__init__('config.json')
        Config._initialized = True

    def get_config(self) -> ConfigDto:
        """return a ConfigDto object"""
        try:
            return ConfigDto(**self._read())
        except TypeError as exc:
            raise MissingArgError() from exc

    def __save_data(self, config) -> None:
        """write a ConfigDto object to file"""
        self._write(config)

    def __is_zone_exist(self, zone_id: str) -> bool:
        """return True if the zone exist in the config file"""
        if zone_id is None:
            return False
        try:
            self.get_config().zones[zone_id]
        except KeyError:
            return False
        return True

    def get_zone(self, zone_id: str) -> ZoneDto:
        """return the ZoneDto corresponding to the zone_id"""
        if not self.__is_zone_exist(zone_id):
            raise ZoneNotFoundError(zone_id)
        return self.get_config().zones[zone_id]

    def get_port(self) -> int:
        return self.get_config().ws_port if self.get_config().ws_port else 5000
