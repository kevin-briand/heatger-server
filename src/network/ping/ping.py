import platform
import socket
import time
from threading import Thread

import scapy.all as scapy

from src.localStorage.config import Config
from src.network.consts import NETWORK, IP
from src.shared.consts.consts import ENABLED
from src.shared.logs.logs import Logs

scanning_in_progress = False


class Ping(Thread):
    def __init__(self, zone_id: str, callback):
        super().__init__()
        self.callback = callback
        self.id = zone_id
        self.stop_ping = True

    def run(self) -> None:
        global scanning_in_progress
        while scanning_in_progress:
            time.sleep(1)
        scanning_in_progress = True

        Logs.info(self.id, 'starting ping...')
        self.stop_ping = False
        if platform.system() == 'Windows':
            self.callback()
            self.stop_ping = True
            return
        network_config = Config().get_config().get(NETWORK)
        ip_list = network_config.get(IP)
        while network_config.get(ENABLED):
            if self.stop_ping:
                scanning_in_progress = False
                return
            ips_found = self.scan(self.get_ip() + '/24')
            for ip in ip_list:
                try:
                    ips_found.index(ip)
                    Logs.info(self.id, F'ip {ip} found !')
                    self.stop_ping = True
                    self.callback()
                    break
                except ValueError:
                    continue

    def stop(self):
        self.stop_ping = True

    def is_running(self) -> bool:
        return not self.stop_ping

    @staticmethod
    def scan(ip) -> [str]:
        arp_req_frame = scapy.ARP(pdst=ip)
        broadcast_ether_frame = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        broadcast_ether_arp_req_frame = broadcast_ether_frame / arp_req_frame

        answered_list = scapy.srp(broadcast_ether_arp_req_frame, timeout=2, verbose=False)[0]
        result = []
        for i in range(0, len(answered_list)):
            result.append(answered_list[i][1].psrc)
        return result

    @staticmethod
    def get_ip() -> str:
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
        if len(ip_split) != 4 or not ip_split[0].isnumeric() or not ip_split[1].isnumeric() or not ip_split[
            2].isnumeric() or not ip_split[3].isnumeric():
            return False
        return True
