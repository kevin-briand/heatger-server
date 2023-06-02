from src.localStorage.dto.configDto import ConfigDto
from src.localStorage.localStorage import LocalStorage
from src.shared.logs.logs import Logs
from src.zone.dto.horaireDto import HoraireDto

CLASSNAME = 'Config'


class Config(LocalStorage):
    def __init__(self):
        super().__init__('config.json')

    def get_config(self):
        return ConfigDto(**self.read())

    def set_config(self, key: str, value: str):
        config = self.get_config()
        config.__setattr__(key, value)
        self.write(config)

    def save_data(self, config):
        self.write(config)

    def add_ip(self, ip: str):
        from src.network.ping.ping import Ping
        if not Ping.is_valid_ip(ip):
            Logs.error(CLASSNAME, 'Bad ip format !')
            return

        config = self.get_config()
        network_config = config.network
        ips_list = network_config.ip
        if ip in ips_list:
            Logs.error(CLASSNAME, 'Ip already exist !')
            return

        ips_list.append(ip)
        self.save_data(config)

    def remove_ip(self, ip: str):
        from src.network.ping.ping import Ping
        if not Ping.is_valid_ip(ip):
            Logs.error(CLASSNAME, 'Bad ip format !')
            return

        config = self.get_config()
        network_config = config.network
        ips_list = network_config.ip
        ips_list.remove(ip)
        self.save_data(config)

    def add_horaire(self, zone_id: str, horaire: HoraireDto):
        if not horaire.is_valid_horaire():
            Logs.error(CLASSNAME, 'Horaire is not valid !')
            return
        config = self.get_config()
        zone = config.__getattribute__(zone_id)
        if zone is None:
            Logs.error(CLASSNAME, 'Zone not found !')
            return
        prog = zone.prog

        if horaire in prog:
            Logs.error(CLASSNAME, 'prog already exist !')
            return
        prog.append(horaire)
        prog.sort(key=Config.sort_horaire)
        self.save_data(config)

    def add_horaires(self, zone_id: str, horaires: [HoraireDto]):
        zone = self.get_config().__getattribute__(zone_id)
        if zone is None:
            Logs.error(CLASSNAME, 'Zone not found !')
            return
        for horaire in horaires:
            self.add_horaire(zone_id, horaire)

    @staticmethod
    def sort_horaire(horaire: HoraireDto) -> int:
        return HoraireDto(horaire.day, horaire.hour, horaire.order).to_value()

    def remove_horaire(self, zone_id: str, horaire: HoraireDto):
        if not horaire.is_valid_horaire():
            Logs.error(CLASSNAME, 'Horaire is not valid !')
            return
        config = self.get_config()
        zone = config.__getattribute__(zone_id)
        if zone is None:
            Logs.error(CLASSNAME, 'Zone not found !')
            return
        prog = zone.prog
        if horaire.horaire_to_object() in prog:
            prog.remove(horaire.horaire_to_object())
            self.save_data(config)

    def remove_all_horaire(self, zone_id: str):
        config = self.get_config()
        zone = config.__getattribute__(zone_id)
        if zone is None:
            Logs.error(CLASSNAME, 'Zone not found !')
            return
        prog = zone.prog
        prog.clear()
        zone.prog = prog

        self.get_config().__setattr__(zone_id, zone)
        self.save_data(config)
