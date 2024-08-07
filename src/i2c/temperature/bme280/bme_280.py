"""BME280 class"""
import bme280
from smbus2 import SMBus

from src.i2c.temperature.dto.sensor_dto import SensorDto
from src.i2c.temperature.temperature import Temperature
from src.localStorage.config.config import Config


class BME280(Temperature):
    """Reading a BME280 temperature"""

    def __init__(self, bus: SMBus):
        super().__init__()
        if not Config().get_config().i2c.temperature.enabled:
            return
        self.device = Config().get_config().i2c.temperature.device
        self.bus = bus
        self.calibration_params = bme280.load_calibration_params(self.bus, self.device.address)

    def get_values(self) -> SensorDto:
        """Read device values, return a SensorDto object"""
        data = bme280.sample(self.bus, self.device.address, self.calibration_params)
        return SensorDto(data.temperature, data.humidity, data.pressure)
