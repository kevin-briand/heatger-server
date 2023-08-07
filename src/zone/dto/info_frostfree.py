"""object for mqtt"""
import json
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.localStorage.jsonEncoder.file_encoder import FileEncoder


@dataclass
class InfoFrostfree:
    """info frostfree data object"""
    next_change: datetime or None

    def to_json(self) -> str:
        """Convert object to json"""
        return json.dumps(self.to_object(), cls=FileEncoder)

    def to_object(self) -> dict[str, Optional[datetime]]:
        """return an object"""
        next_change = None
        if self.next_change is not None:
            next_change = self.next_change.replace(minute=self.next_change.minute,
                                                   second=0, microsecond=0)
        return {"frostfree": next_change}
