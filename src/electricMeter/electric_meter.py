"""ElectricMeter class"""
import json
import time
from threading import Thread

import pigpio

from src.electricMeter.consts import ELECTRIC_METER, CLASSNAME
from src.external.gpio.consts import INPUT
from src.external.gpio.gpio import Gpio
from src.localStorage.config import Config
from src.localStorage.jsonEncoder.file_encoder import FileEncoder
from src.network.mqtt.homeAssistant.consts import PUBLISH_DATA_SENSOR, STATE_NAME
from src.network.network import Network
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
        self.network = Network()
        self.setup_mqtt_if_enabled()
        self.start_if_enabled()

    def start_if_enabled(self) -> None:
        """Start electricity meter if enabled in the configuration file"""
        if Config().get_config().entry.electric_meter.enabled:
            self.start()
            Logs.info(CLASSNAME, "Started !")

    def setup_mqtt_if_enabled(self) -> None:
        """Start mqtt sensor if is enabled in the config file"""
        if Config().get_config().mqtt.enabled:
            self.network.mqtt.init_publish_electric_meter()
            Thread(target=self.refresh_mqtt_datas_loop).start()

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

    def refresh_mqtt_datas_loop(self) -> None:
        """Refresh MQTT datas, send updated datas if necessary"""
        last_counter_send: int = -1
        while True:
            if last_counter_send != self.counter:
                last_counter_send = self.counter
                self.network.mqtt.publish_data(PUBLISH_DATA_SENSOR.replace(STATE_NAME, ELECTRIC_METER),
                                               json.dumps({ELECTRIC_METER: last_counter_send}, cls=FileEncoder))
            time.sleep(0.5)
