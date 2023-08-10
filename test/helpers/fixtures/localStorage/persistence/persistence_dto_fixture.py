from faker import Faker

from src.localStorage.persistence.dto.persistence_dto import PersistenceDto
from test.helpers.fixtures.localStorage.persistence.zone_persistence_dto_fixture import zone_persistence_dto_fixture


def persistence_dto_fixture() -> PersistenceDto:
    fake = Faker()
    return PersistenceDto([zone_persistence_dto_fixture("zone1")],
                          '', fake.uuid4())
