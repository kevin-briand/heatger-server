import json
from datetime import datetime

from src.zone.consts import NAME, STATE, REMAINING_TIME, NEXT_CHANGE, MODE


class InfoZone:
    def __init__(self, id: str, name: str, state: str, next_change: datetime or str, remaining_time: int, mode: str):
        self.id = id
        self.name = name
        self.state = state
        self.next_change = next_change
        self.remaining_time = remaining_time
        self.mode = mode

    def to_json(self):
        next_change: str
        if isinstance(self.next_change, datetime):
            next_change = str(self.next_change.isoformat())
        else:
            next_change = self.next_change
        return json.dumps({F"{self.id}_{NAME}": self.name,
                           F"{self.id}_{STATE}": self.state,
                           F"{self.id}_{NEXT_CHANGE}": next_change,
                           F"{self.id}_{REMAINING_TIME}": str(self.remaining_time),
                           F"{self.id}_{MODE}": str(self.mode)})
