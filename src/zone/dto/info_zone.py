"""object for persistence file"""
import json
from dataclasses import dataclass
from datetime import datetime

from src.shared.enum.mode import Mode
from src.shared.enum.orders import Orders
from src.zone.consts import NAME, STATE, REMAINING_TIME, NEXT_CHANGE, MODE


@dataclass
class InfoZone:
    """infoZone data object"""
    id: str
    name: str
    state: Orders
    next_change: datetime or str
    remaining_time: int
    mode: Mode

    def to_json(self):
        """Convert object to json"""
        next_change: str
        if isinstance(self.next_change, datetime):
            next_change = str(self.next_change.isoformat())
        else:
            next_change = self.next_change
        return json.dumps({F"{self.id}_{NAME}": self.name,
                           F"{self.id}_{STATE}": self.state.name,
                           F"{self.id}_{NEXT_CHANGE}": next_change,
                           F"{self.id}_{REMAINING_TIME}": str(self.remaining_time),
                           F"{self.id}_{MODE}": str(self.mode.name)})
