import json
from datetime import datetime

from src.zone.consts import NAME, STATE, REMAINING_TIME, NEXT_CHANGE


class InfoZone:
    def __init__(self, id: str, name: str, state: str, next_change: datetime, remaining_time: int):
        self.id = id
        self.name = name
        self.state = state
        self.next_change = next_change
        self.remaining_time = remaining_time

    def to_json(self):
        return json.dumps({F"{self.id}_{NAME}": self.name,
                           F"{self.id}_{STATE}": self.state,
                           F"{self.id}_{NEXT_CHANGE}": str(self.next_change.isoformat()),
                           F"{self.id}_{REMAINING_TIME}": str(self.remaining_time)})
