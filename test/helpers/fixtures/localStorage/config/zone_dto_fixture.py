from faker import Faker

from src.zone.dto.zone_dto import ZoneDto


def zone_dto_fixture() -> ZoneDto:
    fake = Faker()
    return ZoneDto(fake.name(), True,
                   fake.random.randint(0, 10), fake.random.randint(10, 20), [])
