"""Config class"""
from typing import Optional

from src.localStorage.dto.config_dto import ConfigDto
from src.localStorage.local_storage import LocalStorage
from src.network.dto.ip_dto import IpDto
from src.shared.logs.logs import Logs
from src.zone.dto.schedule_dto import ScheduleDto

CLASSNAME = 'Config'


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
            return ConfigDto(**self.read())
        except TypeError as exc:
            Logs.error(CLASSNAME, 'missing arguments in the file')
            raise TypeError from exc

    def set_config(self, key: str, value: str) -> None:
        """set value of a key"""
        config = self.get_config()
        setattr(config, key, value)
        self.write(config)

    def save_data(self, config) -> None:
        """write a ConfigDto object to file"""
        print('write')
        self.write(config)

    def add_ip(self, ip: IpDto) -> bool:
        """Adding ip to scanned ip list"""
        from src.network.ping.ping import Ping
        if not Ping.is_valid_ip(ip.ip):
            Logs.error(CLASSNAME, 'Bad ip format !')
            return False

        config = self.get_config()
        network_config = config.network
        ips_list = network_config.ip
        for ip_in_config in ips_list:
            if ip_in_config.ip == ip.ip:
                Logs.error(CLASSNAME, 'Ip already exist !')
                return False

        ips_list.append(ip)
        self.save_data(config)
        return True

    def remove_ip(self, ip: IpDto) -> bool:
        """removing ip to scanned ip list"""
        from src.network.ping.ping import Ping
        if not Ping.is_valid_ip(ip.ip):
            Logs.error(CLASSNAME, 'Bad ip format !')
            return False

        config = self.get_config()
        network_config = config.network
        ips_list = network_config.ip
        ip_with_schedule_removed = []
        for ip_in_config in ips_list:
            if ip_in_config.ip != ip.ip:
                ip_with_schedule_removed.append(ip_in_config)
        network_config.ip = ip_with_schedule_removed
        self.save_data(config)
        return True

    def add_schedule(self, zone_id: str, schedule: ScheduleDto) -> bool:
        """adding schedule to prog list"""
        if not schedule.is_valid_schedule():
            Logs.error(CLASSNAME, 'schedule is not valid !')
            return False
        config = self.get_config()
        zone = getattr(config, zone_id)
        if zone is None:
            Logs.error(CLASSNAME, 'Zone not found !')
            return False
        prog = zone.prog

        for hor in prog:
            if schedule.to_value() == hor.to_value():
                Logs.error(CLASSNAME, 'prog already exist !')
                return False
        prog.append(schedule)
        prog.sort(key=Config.sort_schedule)
        self.save_data(config)
        return True

    def add_schedules(self, zone_id: str, schedules: [ScheduleDto]) -> None:
        """adding schedules list to prog list"""
        zone = getattr(self.get_config(), zone_id)
        if zone is None:
            Logs.error(CLASSNAME, 'Zone not found !')
            return
        for schedule in schedules:
            self.add_schedule(zone_id, schedule)

    @staticmethod
    def sort_schedule(schedule: ScheduleDto) -> int:
        """return schedule to a value"""
        return ScheduleDto(schedule.day, schedule.hour, schedule.state).to_value()

    def remove_schedule(self, zone_id: str, schedule: ScheduleDto) -> bool:
        """removing schedule to prog list"""
        if not schedule.is_valid_schedule():
            Logs.error(CLASSNAME, 'Schedule is not valid !')
            return False
        config = self.get_config()
        zone = getattr(config, zone_id)
        if zone is None:
            Logs.error(CLASSNAME, 'Zone not found !')
            return False
        prog = zone.prog
        prog_with_schedule_removed = []
        for hor in prog:
            if hor.to_value() != schedule.to_value():
                prog_with_schedule_removed.append(hor)
        zone.prog = prog_with_schedule_removed
        self.save_data(config)
        return True

    def remove_all_schedule(self, zone_id: str) -> bool:
        """removing all schedule to prog list"""
        config = self.get_config()
        zone = getattr(config, zone_id)
        if zone is None:
            Logs.error(CLASSNAME, 'Zone not found !')
            return False
        prog = zone.prog
        prog.clear()
        zone.prog = prog

        setattr(self.get_config(), zone_id, zone)
        self.save_data(config)
        return True
