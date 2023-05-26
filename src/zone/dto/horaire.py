import datetime

from src.shared.enum.orders import Orders


class Horaire:
    def __init__(self, day: int, hour: datetime, order: Orders):
        self.day = day
        self.hour = hour
        self.order = order

    @staticmethod
    def array_to_horaire(data: []) -> []:
        list_horaire = []
        for horaire in data:
            hour = int(horaire['hour'].split(':')[0])
            minute = int(horaire['hour'].split(':')[1])
            list_horaire.append(Horaire(int(horaire['day']), datetime.time(hour, minute), Orders.to_order(horaire['order'])))
        return list_horaire
