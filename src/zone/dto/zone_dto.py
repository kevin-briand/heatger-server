"""object for config file"""
import datetime
from dataclasses import dataclass

from src.shared.enum.state import State
from src.zone.dto.horaire_dto import HoraireDto


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
        list_horaire = []
        for horaire in prog:
            hour = int(horaire['hour'].split(':')[0])
            minute = int(horaire['hour'].split(':')[1])
            list_horaire.append(HoraireDto(horaire['day'], datetime.time(hour, minute),
                                           State.to_state(int(horaire['order']))))
        self.prog = list_horaire
