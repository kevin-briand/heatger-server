"""Ping class"""
import socket
import time
from threading import Thread

from scapy.layers.l2 import Ether, ARP, srp

from src.localStorage.config.config import Config
from src.shared.logs.logs import Logs


class Ping(Thread):
    """class for found ip on network"""
    scanning_in_progress = False

    def __init__(self, zone_id: str, callback):
        super().__init__()
        self.callback = callback
        self.zone_id = zone_id
        self.stop_ping = True

    def run(self) -> None:
        while Ping.scanning_in_progress:
            time.sleep(1)
        Ping.scanning_in_progress = True

        Logs.info(self.zone_id, 'starting ping...')
        self.stop_ping = False
        network_config = Config().get_config().network
        ip_list = network_config.ip
        if len(ip_list) == 0:
            Ping.scanning_in_progress = False
            self.callback()
            return
        while network_config.enabled:
            if self.stop_ping:
                Ping.scanning_in_progress = False
                return
            ips_found = self.scan(self.get_ip() + '/24')
            for ip in ip_list:
                try:
                    ips_found.index(ip.ip)
                    Logs.info(self.zone_id, F'device {ip.name} found !')
                    self.stop_ping = True
                    self.callback()
                    break
                except ValueError:
                    continue

    def stop(self):
        """Stop scanning"""
        self.stop_ping = True

    def is_running(self) -> bool:
        """return True if scan is in progress"""
        return not self.stop_ping

    @staticmethod
    def scan(ip) -> [str]:
        """Return a list of ip found on the network"""
        arp_req_frame = ARP(pdst=ip)
        broadcast_ether_frame = Ether(dst="ff:ff:ff:ff:ff:ff")
        broadcast_ether_arp_req_frame = broadcast_ether_frame / arp_req_frame

        answered_list = srp(broadcast_ether_arp_req_frame, timeout=2, verbose=False)[0]
        result = []
        for item in enumerate(answered_list):
            result.append(item[1][1].psrc)
        return result

    @staticmethod
    def get_ip() -> str:
        """return ip of this device or 127.0.0.1"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(0)
        try:
            sock.connect(('10.254.254.254', 1))
            local_ip = sock.getsockname()[0]
        except socket.error:
            local_ip = '127.0.0.1'
        finally:
            sock.close()
        return local_ip

    @staticmethod
    def is_valid_ip(ip: str) -> bool:
        """return True if ip is valid"""
        ip_split = ip.split('.')
        if len(ip_split) != 4 or not ip_split[0].isnumeric()\
                or not ip_split[1].isnumeric() or not ip_split[2].isnumeric()\
                or not ip_split[3].isnumeric():
            return False
        return True
