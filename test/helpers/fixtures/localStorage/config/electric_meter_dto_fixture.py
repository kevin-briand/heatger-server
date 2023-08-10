from faker import Faker

from src.electricMeter.dto.electric_meter_dto import ElectricMeterDto


def electric_meter_dto_fixture() -> ElectricMeterDto:
    fake = Faker()
    return ElectricMeterDto(True, fake.random.randint(0, 30))
