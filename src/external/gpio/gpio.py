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
            return
        self.client.write(addr, status)

    def get_pin(self, addr: int) -> int:
        if platform.system().lower() == WINDOWS:
            return 0
        return self.client.read(addr)

    def init_pin(self, addr: int, mode: int):
        self.client.set_mode(addr, mode)
        resistor = pigpio.PUD_DOWN
        if mode == pigpio.INPUT:
            resistor = pigpio.PUD_UP
        self.client.set_pull_up_down(addr, resistor)

