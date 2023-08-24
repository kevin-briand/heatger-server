from src.i2c.temperature.dto.temperature_dto import TemperatureDto
from test.helpers.fixtures.localStorage.config.device_dto_fixture import device_dto_fixture


def temperature_dto_fixture() -> TemperatureDto:
    return TemperatureDto(True, device_dto_fixture())
