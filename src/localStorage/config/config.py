"""Config class"""
from typing import Optional

from src.localStorage.config.dto.config_dto import ConfigDto
from src.localStorage.config.errors.config_error import ConfigError
from src.localStorage.local_storage import LocalStorage
from src.network.dto.ip_dto import IpDto
from src.shared.errors.file_not_readable_error import FileNotReadableError
from src.shared.errors.file_not_writable_error import FileNotWritableError
from src.zone.dto.schedule_dto import ScheduleDto


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
        except FileNotReadableError as exc:
            raise ConfigError('file not readable') from exc
        except TypeError as exc:
            raise ConfigError('missing arguments in the file') from exc

    def __save_data(self, config) -> None:
        """write a ConfigDto object to file"""
        try:
            self._write(config)
        except FileNotWritableError as exc:
            raise ConfigError('file not writable') from exc

    def add_ip(self, ip: IpDto) -> None:
        """Adding ip to scanned ip list"""
        from src.network.ping.ping import Ping
        if not Ping.is_valid_ip(ip.ip):
            raise ConfigError('Bad ip format !')

        config = self.get_config()
        network_config = config.network
        ips_list = network_config.ip
        if not all(ip_in_list.ip != ip.ip for ip_in_list in ips_list):
            raise ConfigError('Ip already exist !')

        ips_list.append(ip)
        self.__save_data(config)

    def remove_ip(self, ip: IpDto) -> None:
        """removing ip to scanned ip list"""
        from src.network.ping.ping import Ping
        if not Ping.is_valid_ip(ip.ip):
            raise ConfigError('Bad ip format !')

        config = self.get_config()
        network_config = config.network
        ips_list = network_config.ip
        ips_list.remove(ip)
        self.__save_data(config)

    def add_schedule(self, zone_id: str, schedule: ScheduleDto) -> None:
        """adding schedule to prog list"""
        if not schedule.is_valid_schedule():
            raise ConfigError('schedule is not valid !')
        if not self.__is_zone_exist(zone_id):
            raise ConfigError('Zone not found !')

        config = self.get_config()
        zone = getattr(config, zone_id)
        prog: list[ScheduleDto] = zone.prog

        if not all(sch.to_value() != schedule.to_value() for sch in prog):
            raise ConfigError('schedule already exist !')
        prog.append(schedule)
        prog.sort(key=Config._sort_schedule)
        self.__save_data(config)

    def add_schedules(self, zone_id: str, schedules: [ScheduleDto]) -> None:
        """adding schedules list to prog list"""
        if not self.__is_zone_exist(zone_id):
            raise ConfigError('Zone not found !')
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
            raise ConfigError('schedule is not valid !')
        if not self.__is_zone_exist(zone_id):
            raise ConfigError('Zone not found !')

        config = self.get_config()
        zone = getattr(config, zone_id)
        prog = zone.prog
        prog.remove(schedule)
        self.__save_data(config)

    def remove_all_schedule(self, zone_id: str) -> None:
        """removing all schedule to prog list"""
        if not self.__is_zone_exist(zone_id):
            raise ConfigError('Zone not found !')
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
