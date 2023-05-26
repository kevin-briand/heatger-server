import platform
import subprocess

from src.localStorage.config import Config
from src.network.consts import NETWORK, IP
from src.network.mqtt.homeAssistant.homeAssistant import HomeAssistant
from src.shared.consts.consts import ENABLED


class Network:
    def __init__(self):
        config = Config().get_config().get(NETWORK)
        self.ips_list = config.get(IP)
        self.scan_activated = config.get(ENABLED)
        self.mqtt = HomeAssistant()
        self.mqtt.start()

    def scan(self):
        ip_found = False
        while not ip_found and self.scan_activated:
            for ip in self.ips_list:
                if Network.ping(ip):
                    print(F'ip {ip} found !')
                    ip_found = True

    @staticmethod
    def ping(ip: str):
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '1', ip]
        return subprocess.call(command) == 0
