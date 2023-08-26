from faker import Faker

from src.network.dto.network_dto import NetworkDto


def network_dto_fixture() -> NetworkDto:
    fake = Faker()
    return NetworkDto(True, [])
