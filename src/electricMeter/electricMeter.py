import json
import time
from threading import Thread

import pigpio

from src.electricMeter.consts import ELECTRIC_METER, GPIO_INPUT
from src.external.gpio.consts import INPUT
from src.localStorage.consts import INPUT as CONF_INPUT
from src.external.gpio.gpio import Gpio
from src.localStorage.config import Config
from src.shared.consts.consts import ENABLED


class ElectricMeter(Thread):
    def __init__(self):
        super().__init__()
        self.gpio = Gpio()
        config = Config().get_config().get(CONF_INPUT)
        conf_em = config.get(ELECTRIC_METER)
        self.gpio_input = int(conf_em.get(GPIO_INPUT))
        self.run_thread = True
        self.counter = 0
        self.gpio.init_pin(self.gpio_input, INPUT)
        if conf_em.get(ENABLED):
            self.start()

    def run(self) -> None:
        while self.run_thread:
            if self.gpio.get_pin(self.gpio_input) == pigpio.OFF:
                self.counter = self.counter + 1
                while self.gpio.get_pin(self.gpio_input) == pigpio.OFF:
                    time.sleep(0.01)
            time.sleep(0.03)

    def stop(self):
        self.run_thread = False

    def get_total(self):
        return self.counter

    def get_data(self) -> [str]:
        return json.dumps({ELECTRIC_METER: self.counter})
