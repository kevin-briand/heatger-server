"""SensorDto"""
import math
from dataclasses import dataclass


@dataclass
class SensorDto:
    """
    I2C temperature object, return :
     - temperature : in degree Celcius
     - humidity : in percent
     - pressure : in hectoPascal
    """

    def __init__(self, temperature: float, humidity: float, pressure: float):
        self.temperature = int(temperature * 100) / 100
        self.humidity = math.floor(humidity)
        self.pressure = int(pressure * 100) / 100

    def __eq__(self, other: "SensorDto"):
        if other is None:
            return False
        return self.temperature == other.temperature and \
            self.pressure == other.pressure and \
            self.humidity == other.humidity
