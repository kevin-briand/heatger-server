"""PCF8574 class"""
import pcf8574_io

from src.I2C.io.consts import *
from src.I2C.io.enum.button import Button
from src.I2C.io.enum.led_color import LedColor
from src.localStorage.config.config import Config
from src.shared.logs.logs import Logs


class Pcf8574:
    """Reading a PCF8574 chip"""

    def __init__(self):
        super().__init__()
        self.bus = pcf8574_io.PCF(Config().get_config().i2c.io.device.address)
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
        Logs.info(CLASSNAME, "Init...")

    def is_button_pressed(self, button: Button) -> bool:
        """Return True if button is pressed, False if not or if already tested and not released"""
        state_button = not self.bus.read(button.value)
        if getattr(self, button.value) == state_button:
            return False
        setattr(self, button.value, state_button)
        return state_button

    def set_color(self, led_num: int, color: LedColor):
        """Set led color :
            - led : led number(1 or 2)
            - color : color should write
        """
        if not 0 < led_num < len(LedColor)+1:
            Logs.error(CLASSNAME, F'led_num not in the range (min: 1, max: {len(LedColor)})')
            return

        led = LED1 if led_num == 1 else LED2
        self.change_color(led, color)

    def change_color(self, led: list[str], color: LedColor) -> None:
        """Change the color of the given led"""
        for i, led_pin in enumerate(led):
            self.bus.write(led_pin, ON if color.value[i] else OFF)
