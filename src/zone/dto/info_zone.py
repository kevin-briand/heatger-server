"""object for persistence file"""
import json
from dataclasses import dataclass
from datetime import datetime

from src.localStorage.jsonEncoder.file_encoder import FileEncoder
from src.shared.enum.mode import Mode
from src.shared.enum.orders import Orders
from src.zone.consts import NAME, STATE, NEXT_CHANGE, MODE, IS_PING


@dataclass
class InfoZone:
    """infoZone data object"""
    id: str
    name: str
    state: Orders
    next_change: datetime
    is_ping: bool
    mode: Mode

    def to_json(self):
        """Convert object to json"""
        return json.dumps(self.to_object(), cls=FileEncoder)

    def to_object(self):
        """return an object"""
        next_change = None
        if self.next_change is not None:
            next_change = self.next_change.replace(
                minute=self.next_change.minute+1 if self.next_change.minute < 59 else 59,
                second=0, microsecond=0)
        return {F"{self.id}_{NAME}": self.name,
                F"{self.id}_{STATE}": self.state.name,
                F"{self.id}_{NEXT_CHANGE}": next_change,
                F"{self.id}_{MODE}": str(self.mode.name),
                F"{self.id}_{IS_PING}": self.is_ping}
