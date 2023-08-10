from src.localStorage.config.dto.config_dto import ConfigDto
from test.helpers.fixtures.localStorage.config.api_dto_fixture import api_dto_fixture
from test.helpers.fixtures.localStorage.config.entry_dto_fixture import input_dto_fixture
from test.helpers.fixtures.localStorage.config.i2c_dto_fixture import i2c_dto_fixture
from test.helpers.fixtures.localStorage.config.mqtt_dto_fixture import mqtt_dto_fixture
from test.helpers.fixtures.localStorage.config.network_dto_fixture import network_dto_fixture
from test.helpers.fixtures.localStorage.config.zone_dto_fixture import zone_dto_fixture


def config_dto_fixture() -> ConfigDto:
    return ConfigDto(mqtt_dto_fixture(), network_dto_fixture(),
                     i2c_dto_fixture(), input_dto_fixture(),
                     zone_dto_fixture(), zone_dto_fixture(), api_dto_fixture())
