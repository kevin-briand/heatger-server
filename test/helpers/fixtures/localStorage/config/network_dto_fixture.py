from faker import Faker

from src.network.dto.network_dto import NetworkDto
from test.helpers.fixtures.localStorage.config.ip_dto_fixture import ip_dto_fixture


def network_dto_fixture() -> NetworkDto:
    fake = Faker()
    return NetworkDto(True, [ip_dto_fixture()])
