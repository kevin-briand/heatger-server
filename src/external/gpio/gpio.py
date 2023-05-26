import platform

import pigpio

from src.external.gpio.consts import CLASSNAME, WINDOWS
from src.shared.message.message import info


class Gpio:

    @staticmethod
    def set_pin(addr: int, status: bool):
        if platform.system().lower() == WINDOWS:
            info(CLASSNAME, F'set pin : {str(addr)} to {"on" if status else "off"}')
        else:
            pigpio.pi().write(addr, status)
