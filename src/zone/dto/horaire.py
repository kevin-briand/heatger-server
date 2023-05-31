import datetime
from dataclasses import dataclass

from src.shared.enum.orders import Orders


@dataclass
class Horaire:
    day: int
    hour: datetime.time or str
    order: Orders

    @staticmethod
    def array_to_horaire(data: []) -> []:
        list_horaire = []
        for horaire in data:
            hour = int(horaire['hour'].split(':')[0])
            minute = int(horaire['hour'].split(':')[1])
            list_horaire.append(
                Horaire(int(horaire['day']), datetime.time(hour, minute), Orders.to_order(horaire['order'])))
        return list_horaire

    def is_valid_horaire(self) -> bool:
        return 0 <= self.day <= 6 and isinstance(self.hour, datetime.time) and isinstance(self.order, Orders)

    def horaire_to_object(self) -> {}:
        return {'day': self.day,
                'hour': self.hour.strftime('%H:%M'),
                'order': self.order.value}

    def to_value(self) -> int:
        return self.day * 100 + self.hour.hour * 10 + self.hour.minute
