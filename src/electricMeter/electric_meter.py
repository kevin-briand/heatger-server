"""ElectricMeter class"""
import asyncio
import json
import time
from threading import Thread

import pigpio

from src.electricMeter.consts import ELECTRIC_METER, CLASSNAME
from src.external.gpio.consts import INPUT
from src.external.gpio.gpio import Gpio
from src.localStorage.config.config import Config
from src.network.websocket.ws_server import WSServer
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
        if not asyncio.get_event_loop():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        self.loop = asyncio.get_event_loop()
        self.start_if_enabled()

    def start_if_enabled(self) -> None:
        """Start electricity meter if enabled in the configuration file"""
        if Config().get_config().entry.electric_meter.enabled:
            self.start()
            self.setup_ws()
            Logs.info(CLASSNAME, "Started !")

    def setup_ws(self) -> None:
        """Start send data if is enabled in the config file"""
        Thread(target=self.refresh_ws_datas_loop).start()

    def run(self) -> None:
        while self.run_thread:
            if self.gpio.get_pin(self.gpio_input) == pigpio.OFF:
                self.counter = self.counter + 1
                while self.gpio.get_pin(self.gpio_input) == pigpio.OFF:
                    time.sleep(0.01)
            time.sleep(0.03)

    def stop(self) -> None:
        """Stopping reading loop"""
        self.run_thread = False

    def get_total(self) -> int:
        """return the counter"""
        return self.counter

    def get_data(self) -> {ELECTRIC_METER: str}:
        """convert data to json"""
        return json.dumps({ELECTRIC_METER: self.counter})

    def refresh_ws_datas_loop(self) -> None:
        """Refresh WS datas, send updated datas if necessary"""
        while True:
            self.loop.run_until_complete(WSServer.update_electric_meter(self.counter))
            time.sleep(30)
