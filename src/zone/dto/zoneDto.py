import datetime

from src.shared.enum.orders import Orders
from src.zone.dto.horaireDto import HoraireDto


class ZoneDto(object):
    def __init__(self, name: str, enabled: bool, gpio_eco: int, gpio_frostfree: int, prog: [], *args, **kwargs):
        self.name = name
        self.enabled = enabled
        self.gpio_eco = gpio_eco
        self.gpio_frostfree = gpio_frostfree
        list_horaire = []
        for horaire in prog:
            hour = int(horaire['hour'].split(':')[0])
            minute = int(horaire['hour'].split(':')[1])
            list_horaire.append(HoraireDto(horaire['day'], datetime.time(hour, minute),
                                           Orders.to_order(int(horaire['order']))))
        self.prog = list_horaire
