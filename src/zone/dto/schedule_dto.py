"""object for config file"""
import datetime
from dataclasses import dataclass
from datetime import time

from src.shared.enum.state import State


@dataclass
class ScheduleDto:
    """schedule data object"""

    # pylint: disable=unused-argument
    def __init__(self, day, hour: time, state, **kwargs):
        self.day = day
        self.hour = hour
        self.state = state

    def is_valid_schedule(self) -> bool:
        """return True schedule is valid"""
        return 0 <= self.day <= 6 and isinstance(self.hour, time) and isinstance(self.state, State)

    def to_value(self) -> int:
        """return a schedule in value, the bigger it is, the closer it is to the weekend"""
        return self.day * 100 + self.hour.hour * 10 + self.hour.minute

    def to_object(self) -> {}:
        """return schedule into object"""
        return {'day': self.day,
                'hour': self.hour,
                'state': self.state.value}

    def __eq__(self, other: 'ScheduleDto'):
        if other is None:
            return False
        return self.to_value() == other.to_value()

    @staticmethod
    def from_array(data: list) -> list['ScheduleDto']:
        """convert json array to array of scheduleDto"""
        list_horaire = []
        for horaire in data:
            hour = int(horaire['hour'].split(':')[0])
            minute = int(horaire['hour'].split(':')[1])
            list_horaire.append(ScheduleDto(int(horaire['day']),
                                            datetime.time(hour, minute),
                                            State.to_state(horaire['state'])))
        return list_horaire
