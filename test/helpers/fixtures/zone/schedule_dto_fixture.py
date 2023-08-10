import datetime

from faker import Faker

from src.shared.enum.state import State
from src.zone.dto.schedule_dto import ScheduleDto


def schedule_dto_fixture():
    fake = Faker()
    return ScheduleDto(day=fake.random.randint(0, 6),
                       hour=datetime.time(fake.random.randint(0, 23), fake.random.randint(0, 59), 0),
                       state=State.to_state(fake.random.randint(0, State.FROSTFREE.value)))
