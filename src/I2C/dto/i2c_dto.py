"""object for config file"""
from dataclasses import dataclass

from src.I2C.io.dto.io_dto import IODto
from src.I2C.screen.dto.screen_dto import ScreenDto
from src.I2C.temperature.dto.temperature_dto import TemperatureDto


@dataclass
class I2CDto:
    """I2C data object"""

    # pylint: disable=unused-argument
    def __init__(self, temperature, screen, io, **kwargs):
        self.temperature = temperature if isinstance(temperature, TemperatureDto) else TemperatureDto(**temperature)
        self.screen = screen if isinstance(screen, ScreenDto) else ScreenDto(**screen)
        self.io = io if isinstance(io, IODto) else IODto(**io)
