"""BME280 class"""
import bme280
import smbus2

from src.I2C.temperature.consts import PORT, ADDRESS
from src.I2C.temperature.dto.sensor_dto import SensorDto
from src.I2C.temperature.temperature import Temperature
from src.localStorage.config import Config


class BME280(Temperature):
    """Reading a BME280 temperature"""

    def __init__(self):
        super().__init__()
        if Config().get_config().i2c.temperature:
            self.bus = smbus2.SMBus(PORT)
            self.calibration_params = bme280.load_calibration_params(self.bus, ADDRESS)

    def get_values(self) -> SensorDto:
        """Read device values, return a SensorDto object"""
        data = bme280.sample(self.bus, ADDRESS, self.calibration_params)
        return SensorDto(data.temperature, data.humidity, data.pressure)
