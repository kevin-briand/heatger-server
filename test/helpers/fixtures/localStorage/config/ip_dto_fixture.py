from faker import Faker

from src.network.dto.ip_dto import IpDto


def ip_dto_fixture() -> IpDto:
    fake = Faker()
    return IpDto(fake.name(), fake.ipv4())
