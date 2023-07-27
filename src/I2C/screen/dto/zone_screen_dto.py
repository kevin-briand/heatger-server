"""object for screen"""
from dataclasses import dataclass

from src.shared.enum.state import State


@dataclass
class ZoneScreenDto:
    """zones data object for screen"""

    def __init__(self, zone1_state: State, zone2_state: State, zone1_name: str, zone2_name: str):
        self.zone1_state = zone1_state
        self.zone2_state = zone2_state
        self.zone1_name = zone1_name
        self.zone2_name = zone2_name
