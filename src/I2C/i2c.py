"""I2C manager"""
import json
import time
from threading import Thread
from typing import Optional

from src.I2C.temperature.bme280.bme_280 import BME280
from src.I2C.temperature.dto.sensor_dto import SensorDto
from src.localStorage.config import Config
from src.localStorage.jsonEncoder.file_encoder import FileEncoder
from src.network.mqtt.homeAssistant.consts import PUBLISH_DATA_SENSOR, STATE_NAME
from src.network.network import Network
from src.I2C.consts import I2C as I2C_CONST


class I2C(Thread):
    """I2C Manager class, run a event loop for update I2C devices"""
    def __init__(self):
        super().__init__()
        self.run_loop = True
        self.temperature_sensor = BME280()
        self.temperature: Optional[SensorDto] = None
        self.network = Network()
        if Config().get_config().mqtt.enabled:
            self.network.mqtt.init_publish_i2c()
            Thread(target=self.refresh_mqtt_datas).start()

    def run(self) -> None:
        config_i2c = Config().get_config().i2c
        if not config_i2c.temperature.enabled \
                and not config_i2c.io.enabled \
                and not config_i2c.screen.enabled:
            return

        if config_i2c.temperature.enabled:
            self.temperature = self.temperature_sensor.get_values()

        iterations = 0
        while self.run_loop:
            if iterations == 60 and config_i2c.temperature.enabled:
                self.temperature = self.temperature_sensor.get_values()
                iterations = 0
            iterations += 1
            time.sleep(0.5)

    def refresh_mqtt_datas(self):
        """Refresh MQTT datas, send updated datas if necessary"""
        data: Optional[SensorDto] = None
        while True:
            if self.temperature is not None and data != self.temperature:
                data = self.temperature
                self.network.mqtt.publish_data(PUBLISH_DATA_SENSOR.replace(STATE_NAME, I2C_CONST),
                                               json.dumps(data, cls=FileEncoder))
            time.sleep(0.5)

    def stop(self):
        """Stop event loop"""
        self.run_loop = False
