from src.I2C.io.dto.ioDto import IODto
from src.I2C.screen.dto.screenDto import ScreenDto
from src.I2C.temperature.dto.temperatureDto import TemperatureDto


class I2CDto(object):
    def __init__(self, temperature, screen, io, *args, **kwargs):
        self.temperature = TemperatureDto(**temperature)
        self.screen = ScreenDto(**screen)
        self.io = IODto(**io)
