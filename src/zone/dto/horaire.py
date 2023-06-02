import datetime

from src.shared.enum.orders import Orders
from src.zone.dto.horaireDto import HoraireDto


class Horaire:
    @staticmethod
    def array_to_horaire(data: []) -> [HoraireDto]:
        list_horaire = []
        for horaire in data:
            hour = int(horaire['hour'].split(':')[0])
            minute = int(horaire['hour'].split(':')[1])
            list_horaire.append(
                HoraireDto(int(horaire['day']), datetime.time(hour, minute), Orders.to_order(horaire['order'])))
        return list_horaire
