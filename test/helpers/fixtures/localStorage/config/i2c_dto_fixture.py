from src.I2C.dto.i2c_dto import I2CDto
from test.helpers.fixtures.localStorage.config.io_dto_fixture import io_dto_fixture
from test.helpers.fixtures.localStorage.config.screen_dto_fixture import screen_dto_fixture
from test.helpers.fixtures.localStorage.config.temperature_dto_fixture import temperature_dto_fixture


def i2c_dto_fixture() -> I2CDto:
    return I2CDto(temperature_dto_fixture(), screen_dto_fixture(), io_dto_fixture())
