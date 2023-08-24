from faker import Faker

from src.i2c.dto.device_dto import DeviceDto


def device_dto_fixture() -> DeviceDto:
    fake = Faker()
    return DeviceDto(F"0x{fake.random.randint(0, 9)}{fake.random.randint(0, 9)}", fake.random.randint(0, 2))
