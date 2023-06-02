from datetime import time

from src.shared.enum.orders import Orders


class HoraireDto(object):
    def __init__(self, day, hour: time, order, *args, **kwargs):
        self.day = day
        self.hour = hour
        self.order = order

    def is_valid_horaire(self) -> bool:
        return 0 <= self.day <= 6 and isinstance(self.hour, time) and isinstance(self.order, Orders)

    def to_value(self) -> int:
        return self.day * 100 + self.hour.hour * 10 + self.hour.minute

    def horaire_to_object(self) -> {}:
        return {'day': self.day,
                'hour': self.hour,
                'order': self.order.value}
