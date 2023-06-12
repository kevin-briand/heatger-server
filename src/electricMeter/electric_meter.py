"""ElectricMeter class"""
import json
import time
from threading import Thread

import pigpio

from src.electricMeter.consts import ELECTRIC_METER, CLASSNAME
from src.external.gpio.consts import INPUT
from src.external.gpio.gpio import Gpio
from src.localStorage.config import Config
from src.shared.logs.logs import Logs


class ElectricMeter(Thread):
    """Class for reading and counting a GPIO input"""
    def __init__(self):
        super().__init__()
        self.gpio = Gpio()
        conf_em = Config().get_config().entry.electric_meter
        self.gpio_input = int(conf_em.gpio_input)
        self.run_thread = True
        self.counter = 0
        self.gpio.init_pin(self.gpio_input, INPUT)
        if conf_em.enabled:
            self.start()
            Logs.info(CLASSNAME, "Started !")

    def run(self) -> None:
        while self.run_thread:
            if self.gpio.get_pin(self.gpio_input) == pigpio.OFF:
                self.counter = self.counter + 1
                while self.gpio.get_pin(self.gpio_input) == pigpio.OFF:
                    time.sleep(0.01)
            time.sleep(0.03)

    def stop(self):
        """Stopping reading loop"""
        self.run_thread = False

    def get_total(self):
        """return the counter"""
        return self.counter

    def get_data(self) -> [str]:
        """convert data to json"""
        return json.dumps({ELECTRIC_METER: self.counter})
