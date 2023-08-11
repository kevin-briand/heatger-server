"""Config class"""
from typing import Optional

from src.localStorage.config.dto.config_dto import ConfigDto
from src.localStorage.config.errors.already_exist_error import AlreadyExistError
from src.localStorage.config.errors.bad_ip_format_error import BadIpFormatError
from src.localStorage.config.errors.config_error import ConfigError
from src.localStorage.config.errors.schedule_not_valid_error import ScheduleNotValidError
from src.localStorage.config.errors.zone_not_found_error import ZoneNotFoundError
from src.localStorage.errors.missing_arg_error import MissingArgError
from src.localStorage.local_storage import LocalStorage
from src.network.dto.ip_dto import IpDto
from src.zone.dto.schedule_dto import ScheduleDto
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

    def add_ip(self, ip: IpDto) -> None:
        """Adding ip to scanned ip list"""
        from src.network.ping.ping import Ping
        if not Ping.is_valid_ip(ip.ip):
            raise BadIpFormatError(ip.ip)

        config = self.get_config()
        network_config = config.network
        ips_list = network_config.ip
        if not all(ip_in_list.ip != ip.ip for ip_in_list in ips_list):
            raise AlreadyExistError(ip.ip)

        ips_list.append(ip)
        self.__save_data(config)

    def remove_ip(self, ip: IpDto) -> None:
        """removing ip to scanned ip list"""
        from src.network.ping.ping import Ping
        if not Ping.is_valid_ip(ip.ip):
            raise BadIpFormatError(ip.ip)

        config = self.get_config()
        network_config = config.network
        ips_list = network_config.ip
        ips_list.remove(ip)
        self.__save_data(config)

    def add_schedule(self, zone_id: str, schedule: ScheduleDto) -> None:
        """adding schedule to prog list"""
        if not schedule.is_valid_schedule():
            raise ScheduleNotValidError()
        if not self.__is_zone_exist(zone_id):
            raise ZoneNotFoundError(zone_id)

        config = self.get_config()
        zone = getattr(config, zone_id)
        prog: list[ScheduleDto] = zone.prog

        if not all(sch.to_value() != schedule.to_value() for sch in prog):
            raise AlreadyExistError('Schedule')
        prog.append(schedule)
        prog.sort(key=Config._sort_schedule)
        self.__save_data(config)

    def add_schedules(self, zone_id: str, schedules: [ScheduleDto]) -> None:
        """adding schedules list to prog list"""
        if not self.__is_zone_exist(zone_id):
            raise ZoneNotFoundError(zone_id)
        for schedule in schedules:
            try:
                self.add_schedule(zone_id, schedule)
            except ConfigError:
                pass

    @staticmethod
    def _sort_schedule(schedule: ScheduleDto) -> int:
        """return schedule to a value"""
        return ScheduleDto(schedule.day, schedule.hour, schedule.state).to_value()

    def remove_schedule(self, zone_id: str, schedule: ScheduleDto) -> None:
        """removing schedule to prog list"""
        if not schedule.is_valid_schedule():
            raise ScheduleNotValidError()
        if not self.__is_zone_exist(zone_id):
            raise ZoneNotFoundError(zone_id)

        config = self.get_config()
        zone = getattr(config, zone_id)
        prog = zone.prog
        prog.remove(schedule)
        self.__save_data(config)

    def remove_all_schedule(self, zone_id: str) -> None:
        """removing all schedule to prog list"""
        if not self.__is_zone_exist(zone_id):
            raise ZoneNotFoundError(zone_id)
        config = self.get_config()
        zone = getattr(config, zone_id)
        prog = zone.prog
        prog.clear()
        zone.prog = prog

        setattr(self.get_config(), zone_id, zone)
        self.__save_data(config)

    def __is_zone_exist(self, zone_id: str) -> bool:
        """return True if the zone exist in the config file"""
        if zone_id is None:
            return False
        return getattr(self.get_config(), zone_id, None) is not None

    def get_zone(self, zone_id: str) -> ZoneDto:
        """return the ZoneDto corresponding to the zone_id"""
        if not self.__is_zone_exist(zone_id):
            raise ZoneNotFoundError(zone_id)
        return getattr(self.get_config(), zone_id)
