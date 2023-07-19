"""PCF8574 class"""
import pcf8574_io

from src.I2C.io.consts import *
from src.I2C.io.enum.button import Button
from src.I2C.io.enum.led_color import LedColor
from src.shared.logs.logs import Logs


class Pcf8574:
    """Reading a PCF8574 chip"""

    def __init__(self):
        super().__init__()
        self.bus = pcf8574_io.PCF(ADDRESS)
        self.bus.pin_mode(PIN_LED_1_1, OUTPUT)
        self.bus.pin_mode(PIN_LED_1_2, OUTPUT)
        self.bus.pin_mode(PIN_LED_1_3, OUTPUT)
        self.bus.pin_mode(PIN_LED_2_1, OUTPUT)
        self.bus.pin_mode(PIN_LED_2_2, OUTPUT)
        self.bus.pin_mode(PIN_LED_2_3, OUTPUT)
        self.bus.pin_mode(PIN_BP_1, INPUT)
        self.bus.pin_mode(PIN_BP_2, INPUT)
        self.p6 = False
        self.p7 = False
        Logs.info(CLASSNAME, "Init IO...")

    def is_bp_pressed(self, bp: Button) -> bool:
        """Return True if button is pressed, False if not or if already tested and not released"""
        state_bp = not self.bus.read(bp.value)
        if getattr(self, bp.value) == state_bp:
            return False
        if state_bp:
            setattr(self, bp.value, True)
            return True
        setattr(self, bp.value, False)
        return False

    def set_color(self, led: int, color: LedColor):
        """Set led color :
            - led : led number(1 or 2)
            - color : color should write
        """
        if led == 1:
            self.bus.write(PIN_LED_1_1, ON if color.value[0] else OFF)
            self.bus.write(PIN_LED_1_2, ON if color.value[1] else OFF)
            self.bus.write(PIN_LED_1_3, ON if color.value[2] else OFF)
        elif led == 2:
            self.bus.write(PIN_LED_2_1, ON if color.value[0] else OFF)
            self.bus.write(PIN_LED_2_2, ON if color.value[1] else OFF)
            self.bus.write(PIN_LED_2_3, ON if color.value[2] else OFF)
        else:
            Logs.error(CLASSNAME, F"unknown led number !({led})")
