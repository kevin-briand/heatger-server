from src.shared.enum.orders import Orders

from src.external.gpiozero.gpio import Gpio
from src.shared.message.message import info

CLASSNAME = 'Pilot'


class Pilot:
    def __init__(self, gpio_eco_addr, gpio_frostfree_addr, reverse_on=False):
        self.gpio = Gpio()
        self.gpio_eco_addr = gpio_eco_addr
        self.gpio_frostfree_addr = gpio_frostfree_addr
        self.on = reverse_on
        self.reset_pins()

    def set_order(self, order: Orders):
        info(CLASSNAME, 'Pilot - set order : ' + order.name)
        self.reset_pins()
        gpio_addr = self.gpio_eco_addr
        if order == Orders.COMFORT:
            return
        elif order == Orders.FROSTFREE:
            gpio_addr = self.gpio_frostfree_addr
        self.gpio.set_pin(gpio_addr, self.on)

    def reset_pins(self):
        self.gpio.set_pin(self.gpio_eco_addr, not self.on)
        self.gpio.set_pin(self.gpio_frostfree_addr, not self.on)
