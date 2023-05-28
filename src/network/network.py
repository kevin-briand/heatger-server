import socket

import scapy.all as scapy

from src.localStorage.config import Config
from src.network.consts import NETWORK, IP
from src.network.mqtt.consts import MQTT
from src.network.mqtt.homeAssistant.homeAssistant import HomeAssistant
from src.shared.consts.consts import ENABLED


class Network:
    def __init__(self):
        self.mqtt = HomeAssistant()
        if Config().get_config().get(MQTT).get(ENABLED):
            self.mqtt.start()

    @staticmethod
    def scan(ip):
        arp_req_frame = scapy.ARP(pdst=ip)
        broadcast_ether_frame = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        broadcast_ether_arp_req_frame = broadcast_ether_frame / arp_req_frame

        answered_list = scapy.srp(broadcast_ether_arp_req_frame, timeout=2, verbose=False)[0]
        result = []
        for i in range(0, len(answered_list)):
            result.append(answered_list[i][1].psrc)
        return result

    def scan_ips_list(self):
        ip_found = False
        network_config = Config().get_config().get(NETWORK)
        ip_list = network_config.get(IP)
        while not ip_found and network_config.get(ENABLED):
            ips_found = self.scan(self.get_ip() + '/24')
            for ip in ip_list:
                if ips_found.index(ip) >= 0:
                    print(F'ip {ip} found !')
                    ip_found = True
                    break

    @staticmethod
    def get_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        try:
            s.connect(('10.254.254.254', 1))
            local_ip = s.getsockname()[0]
        except Exception:
            local_ip = '127.0.0.1'
        finally:
            s.close()
        return local_ip

    @staticmethod
    def is_valid_ip(ip: str) -> bool:
        ip_split = ip.split('.')
        if len(ip_split) != 4 or not ip_split[0].isnumeric() or not ip_split[1].isnumeric() or not ip_split[2].isnumeric() or not ip_split[3].isnumeric():
            return False
        return True
