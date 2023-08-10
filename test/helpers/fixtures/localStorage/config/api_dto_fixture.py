from faker import Faker

from src.network.api.dto.api_dto import ApiDto


def api_dto_fixture() -> ApiDto:
    fake = Faker()
    return ApiDto(fake.name(), fake.name())
