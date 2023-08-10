"""object for config file"""
import datetime
from dataclasses import dataclass
from typing import List

from src.shared.enum.state import State
from src.zone.dto.schedule_dto import ScheduleDto


@dataclass
class ZoneDto:
    """zone data object"""

    # pylint: disable=unused-argument
    def __init__(self, name: str, enabled: bool,
                 gpio_eco: int, gpio_frostfree: int, prog: [], **kwargs):
        self.name = name
        self.enabled = enabled
        self.gpio_eco = gpio_eco
        self.gpio_frostfree = gpio_frostfree
        schedules = []
        if self.is_list_of_schedule_dto(prog):
            schedules = prog
        else:
            for schedule in prog:
                hour = int(schedule['hour'].split(':')[0])
                minute = int(schedule['hour'].split(':')[1])
                schedules.append(ScheduleDto(schedule['day'], datetime.time(hour, minute),
                                             State.to_state(int(schedule['state']))))
        self.prog = schedules

    @staticmethod
    def is_list_of_schedule_dto(obj: list) -> bool:
        """return true if the given list is a list of ScheduleDto"""
        return isinstance(obj, List) and all(isinstance(item, ScheduleDto) for item in obj)
