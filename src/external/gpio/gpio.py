import platform

import pigpio

from src.external.gpio.consts import CLASSNAME, WINDOWS
from src.shared.logs.logs import Logs


class Gpio:
    def __init__(self):
        if platform.system().lower() != WINDOWS:
            self.client = pigpio.pi()

    def set_pin(self, addr: int, status: bool):
        if platform.system().lower() == WINDOWS:
            Logs.info(CLASSNAME, F'set pin : {str(addr)} to {"on" if status else "off"}')
        else:
            self.client.write(addr, status)
