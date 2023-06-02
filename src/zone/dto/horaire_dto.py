"""object for config file"""
import datetime
from dataclasses import dataclass
from datetime import time

from src.shared.enum.orders import Orders


@dataclass
class HoraireDto:
    """horaire data object"""

    # pylint: disable=unused-argument
    def __init__(self, day, hour: time, order, *args, **kwargs):
        self.day = day
        self.hour = hour
        self.order = order

    def is_valid_horaire(self) -> bool:
        """return True horaire is valid"""
        return 0 <= self.day <= 6 and isinstance(self.hour, time) and isinstance(self.order, Orders)

    def to_value(self) -> int:
        """return a horaire in value, the bigger it is, the closer it is to the weekend"""
        return self.day * 100 + self.hour.hour * 10 + self.hour.minute

    def horaire_to_object(self) -> {}:
        """return horaire into object"""
        return {'day': self.day,
                'hour': self.hour,
                'order': self.order.value}

    @staticmethod
    def array_to_horaire(data: []) -> []:
        """convert json array to array of HoraireDto"""
        list_horaire = []
        for horaire in data:
            hour = int(horaire['hour'].split(':')[0])
            minute = int(horaire['hour'].split(':')[1])
            list_horaire.append(HoraireDto(int(horaire['day']),
                                           datetime.time(hour, minute),
                                           Orders.to_order(horaire['order'])))
        return list_horaire
