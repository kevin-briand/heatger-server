from src.i2c.io.dto.io_dto import IODto
from test.helpers.fixtures.localStorage.config.device_dto_fixture import device_dto_fixture


def io_dto_fixture() -> IODto:
    return IODto(True, device_dto_fixture())
