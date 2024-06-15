"""Pilot class"""
from src.external.gpio.consts import OUTPUT
from src.shared.enum.state import State

from src.external.gpio.gpio import Gpio
from src.shared.logs.logs import Logs

CLASSNAME = 'Pilot'


class Pilot:
    """Class used for manage GPIO pins :\n
     1 init pins to output\n
     2 set all pins to OFF\n
     3 set 1 pin to ON (if necessary)
    """
    gpio = None

    def __init__(self, gpio_eco_addr, gpio_frostfree_addr, reverse_on=False):
        if not Pilot.gpio:
            Pilot.gpio = Gpio()
        self.gpio_eco_addr = gpio_eco_addr
        self.gpio_frostfree_addr = gpio_frostfree_addr
        self.on = reverse_on
        self.reset_pins()
        Pilot.gpio.init_pin(gpio_eco_addr, OUTPUT)
        Pilot.gpio.init_pin(gpio_frostfree_addr, OUTPUT)

    def set_state(self, order: State):
        """Set order (Orders enum)"""
        Logs.info(CLASSNAME, 'set order : ' + order.name)
        self.reset_pins()
        gpio_addr = self.gpio_eco_addr
        if order == State.COMFORT:
            return
        if order == State.FROSTFREE:
            gpio_addr = self.gpio_frostfree_addr
        Pilot.gpio.set_pin(gpio_addr, self.on)

    def reset_pins(self):
        """Reset pins to off"""
        Pilot.gpio.set_pin(self.gpio_eco_addr, not self.on)
        Pilot.gpio.set_pin(self.gpio_frostfree_addr, not self.on)
