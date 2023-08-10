from src.localStorage.config.dto.config_dto import InputDto
from test.helpers.fixtures.localStorage.config.electric_meter_dto_fixture import electric_meter_dto_fixture


def input_dto_fixture() -> InputDto:
    return InputDto(electric_meter_dto_fixture())
