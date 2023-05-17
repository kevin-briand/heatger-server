import datetime

from src.shared.enum.orders import Orders


class Horaire:
    def __init__(self, day: int, hour: datetime, order: Orders):
        self.day = day
        self.hour = hour
        self.order = order
