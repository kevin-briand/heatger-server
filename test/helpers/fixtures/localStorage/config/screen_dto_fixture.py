from src.i2c.screen.dto.screen_dto import ScreenDto
from test.helpers.fixtures.localStorage.config.device_dto_fixture import device_dto_fixture


def screen_dto_fixture() -> ScreenDto:
    return ScreenDto(True, device_dto_fixture())
