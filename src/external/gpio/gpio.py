"""GPIO class"""
import platform

import pigpio

from src.external.gpio.consts import CLASSNAME, WINDOWS
from src.shared.logs.logs import Logs


class Gpio:
    """Class for reading and writing GPIO header"""
    def __init__(self):
        if platform.system().lower() != WINDOWS:
            self.client = pigpio.pi()

    def set_pin(self, addr: int, status: bool) -> None:
        """set GPIO pin on or off"""
        if platform.system().lower() == WINDOWS:
            Logs.info(CLASSNAME, F'set pin : {str(addr)} to {"on" if status else "off"}')
            return
        self.client.write(addr, status)

    def get_pin(self, addr: int) -> int:
        """get GPIO pin state(0 or 1)"""
        if platform.system().lower() == WINDOWS:
            return 0
        return self.client.read(addr)

    def init_pin(self, addr: int, mode: int) -> None:
        """initialise GPIO pin for input or output use"""
        if platform.system().lower() == WINDOWS:
            return
        self.client.set_mode(addr, mode)
        resistor = pigpio.PUD_DOWN
        if mode == pigpio.INPUT:
            resistor = pigpio.PUD_UP
        self.client.set_pull_up_down(addr, resistor)
