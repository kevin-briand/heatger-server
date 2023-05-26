import platform
import subprocess


class Network:
    def __init__(self, ips_list, scan_activated=False):
        self.ips_list = ips_list
        self.scan_activated = scan_activated

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
