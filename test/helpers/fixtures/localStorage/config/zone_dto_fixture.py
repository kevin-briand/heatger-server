from faker import Faker

from src.zone.dto.zone_dto import ZoneDto
from test.helpers.fixtures.zone.schedule_dto_fixture import schedule_dto_fixture


def zone_dto_fixture() -> ZoneDto:
    fake = Faker()
    return ZoneDto(fake.name(), True,
                   fake.random.randint(0, 10), fake.random.randint(10, 20),
                   [schedule_dto_fixture(), schedule_dto_fixture()])
