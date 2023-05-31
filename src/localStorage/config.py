from datetime import time

from src.localStorage.localStorage import LocalStorage
from src.network.consts import NETWORK, IP
from src.shared.logs.logs import Logs
from src.zone.consts import PROG
from src.zone.dto.horaire import Horaire

CLASSNAME = 'Config'


class Config(LocalStorage):
    def __init__(self):
        super().__init__('config.json')
        self.config = self.read()

    def get_config(self) -> dict:
        return self.config

    def set_config(self, key: str, value: str):
        self.config[key] = value
        self.write(self.config)

    def add_ip(self, ip: str):
        from src.network.ping.ping import Ping
        if not Ping.is_valid_ip(ip):
            Logs.error(CLASSNAME, 'Bad ip format !')
            return

        network_config = self.get_config().get(NETWORK)
        ips_list = network_config.get(IP)
        if ip in ips_list:
            Logs.error(CLASSNAME, 'Ip already exist !')
            return

        ips_list.append(ip)
        self.set_config(NETWORK, network_config)

    def remove_ip(self, ip: str):
        from src.network.ping.ping import Ping
        if not Ping.is_valid_ip(ip):
            Logs.error(CLASSNAME, 'Bad ip format !')
            return

        network_config = self.get_config().get(NETWORK)
        ips_list = network_config.get(IP)
        ips_list.remove(ip)
        self.set_config(NETWORK, network_config)

    def add_horaire(self, zone_id: str, horaire: Horaire):
        if not horaire.is_valid_horaire():
            Logs.error(CLASSNAME, 'Horaire is not valid !')
            return
        zone = self.get_config().get(zone_id)
        if zone is None:
            Logs.error(CLASSNAME, 'Zone not found !')
            return
        prog = zone.get(PROG)

        if horaire.horaire_to_object() in prog:
            Logs.error(CLASSNAME, 'prog already exist !')
            return
        prog.append(horaire.horaire_to_object())
        prog.sort(key=Config.sort_horaire)
        self.set_config(zone_id, zone)

    def sort_horaire(horaire: {}) -> int:
        hour = time(int(horaire.get('hour').split(':')[0]), int(horaire.get('hour').split(':')[1]))
        return Horaire(horaire.get('day'), hour, horaire.get('order')).to_value()

    def remove_horaire(self, zone_id: str, horaire: Horaire):
        if not horaire.is_valid_horaire():
            Logs.error(CLASSNAME, 'Horaire is not valid !')
            return
        zone = self.get_config().get(zone_id)
        if zone is None:
            Logs.error(CLASSNAME, 'Zone not found !')
            return
        prog = zone.get(PROG)
        if horaire.horaire_to_object() in prog:
            prog.remove(horaire.horaire_to_object())
            self.set_config(zone_id, zone)

    def remove_all_horaire(self, zone_id: str):
        zone = self.get_config().get(zone_id)
        if zone is None:
            Logs.error(CLASSNAME, 'Zone not found !')
            return
        prog = zone.get(PROG)
        prog.clear()
        self.set_config(zone_id, zone)

    def add_horaires(self, zone_id: str, horaires: [Horaire]):
        zone = self.get_config().get(zone_id)
        if zone is None:
            Logs.error(CLASSNAME, 'Zone not found !')
            return
        for horaire in horaires:
            self.add_horaire(zone_id, horaire)
