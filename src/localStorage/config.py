"""Config class"""
from src.localStorage.dto.config_dto import ConfigDto
from src.localStorage.local_storage import LocalStorage
from src.network.dto.ip_dto import IpDto
from src.shared.logs.logs import Logs
from src.zone.dto.horaire_dto import HoraireDto

CLASSNAME = 'Config'


class Config(LocalStorage):
    """Class for reading/writing the configuration in file"""
    def __init__(self):
        super().__init__('config.json')

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
        ip_with_horaire_removed = []
        for ip_in_config in ips_list:
            if ip_in_config.ip != ip.ip:
                ip_with_horaire_removed.append(ip_in_config)
        network_config.ip = ip_with_horaire_removed
        self.save_data(config)
        return True

    def add_horaire(self, zone_id: str, horaire: HoraireDto) -> bool:
        """adding horaire to prog list"""
        if not horaire.is_valid_horaire():
            Logs.error(CLASSNAME, 'Horaire is not valid !')
            return False
        config = self.get_config()
        zone = getattr(config, zone_id)
        if zone is None:
            Logs.error(CLASSNAME, 'Zone not found !')
            return False
        prog = zone.prog

        for hor in prog:
            if horaire.to_value() == hor.to_value():
                Logs.error(CLASSNAME, 'prog already exist !')
                return False
        prog.append(horaire)
        prog.sort(key=Config.sort_horaire)
        self.save_data(config)
        return True

    def add_horaires(self, zone_id: str, horaires: [HoraireDto]) -> None:
        """adding horaire list to prog list"""
        zone = getattr(self.get_config(), zone_id)
        if zone is None:
            Logs.error(CLASSNAME, 'Zone not found !')
            return
        for horaire in horaires:
            self.add_horaire(zone_id, horaire)

    @staticmethod
    def sort_horaire(horaire: HoraireDto) -> int:
        """return horaire to a value"""
        return HoraireDto(horaire.day, horaire.hour, horaire.order).to_value()

    def remove_horaire(self, zone_id: str, horaire: HoraireDto) -> bool:
        """removing horaire to prog list"""
        if not horaire.is_valid_horaire():
            Logs.error(CLASSNAME, 'Horaire is not valid !')
            return False
        config = self.get_config()
        zone = getattr(config, zone_id)
        if zone is None:
            Logs.error(CLASSNAME, 'Zone not found !')
            return False
        prog = zone.prog
        prog_with_horaire_removed = []
        for hor in prog:
            if hor.to_value() != horaire.to_value():
                prog_with_horaire_removed.append(hor)
        zone.prog = prog_with_horaire_removed
        self.save_data(config)
        return True

    def remove_all_horaire(self, zone_id: str) -> bool:
        """removing all horaire to prog list"""
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
