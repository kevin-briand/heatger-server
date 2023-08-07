"""object for persistence file"""
from dataclasses import dataclass
from typing import Union

from src.shared.enum.mode import Mode
from src.shared.enum.state import State


@dataclass
class ZonePersistenceDto:
    """zone persistence data object"""

    # pylint: disable=unused-argument
    def __init__(self, zone_id: str, state: Union[State, int], mode: Union[Mode, int], **kwargs):
        self.id = zone_id
        self.state = State(state) if isinstance(state, int) else state
        self.mode = Mode(mode) if isinstance(mode, int) else mode

    def __eq__(self, other: 'ZonePersistenceDto') -> bool:
        if other is None:
            return False
        return self.id == other.id
