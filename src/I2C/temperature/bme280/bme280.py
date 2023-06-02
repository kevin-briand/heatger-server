"""BME280 class"""
from src.I2C.temperature.temperature import Temperature


class BME280(Temperature):
    """Reading a BME280 temperature"""
    def get_values(self) -> []:
        """get values"""
