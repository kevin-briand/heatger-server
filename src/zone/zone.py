from array import array

from src.network.network import Network
from src.pilot.pilot import Pilot
from src.shared.enum.orders import Orders
from src.shared.timer.timer import Timer
from src.zone.dto.horaire import Horaire
from datetime import datetime, timedelta


def get_next_day(weekday: int, hour: datetime) -> datetime:
    now = datetime.now()
    actual_weekday = datetime.now().weekday()
    if actual_weekday > weekday:
        next_day = ((7 - actual_weekday) + weekday)
    elif actual_weekday == weekday and (hour.hour < now.hour or (hour.hour >= now.hour and hour.minute < now.minute)):
        next_day = 7
    else:
        next_day = (weekday - actual_weekday)

    td = timedelta(days=next_day)
    result = datetime.fromtimestamp(datetime.now().timestamp() + td.total_seconds())
    return result.replace(hour=hour.hour, minute=hour.minute, second=0, microsecond=0)


class Zone:
    def __init__(self, name: str, network=None, list_horaires=None, clock_activated=False):
        print('Init Zone ' + name)
        if list_horaires is None:
            list_horaires = []
        self.name = name
        self.timer = Timer()
        self.current_order = Orders.COMFORT
        self.next_order = Orders.ECO
        self.clock_activated = clock_activated
        self.list_horaires = list_horaires
        self.current_horaire = None
        self.pilot = Pilot(11, 12, True)
        self.network = network
        if clock_activated and list_horaires is not None:
            self.start_next_order()

    def set_list_horaires(self, list_horaires):
        self.list_horaires: array = list_horaires
        if self.clock_activated and list_horaires is not None:
            self.start_next_order()

    def on_time_out(self):
        print('timeOut zone ' + self.name + ' switch ' + self.current_order.name + ' to ' + self.next_order.name)
        print('starting ping...')
        self.network.scan()
        self.set_order(self.next_order)
        self.start_next_order()

    def start_next_order(self):
        next_horaire: Horaire = None
        remaining_time: int = 0
        horaire_date: datetime
        now = datetime.now()
        for horaire in self.list_horaires:
            horaire_date = get_next_day(horaire.day, horaire.hour)
            print(horaire_date)
            if horaire.day >= now.weekday() and horaire_date > datetime.now() and horaire is not self.current_horaire:
                next_horaire = horaire
                remaining_time = int(horaire_date.timestamp() - now.timestamp())
                break
        if next_horaire is None:
            if len(self.list_horaires) > 0:
                horaire_date = get_next_day(self.list_horaires[0].day, self.list_horaires[0].hour)
                next_horaire = self.list_horaires[0]
                remaining_time = int(horaire_date.timestamp() - now.timestamp())
            else:
                return

        self.current_horaire = next_horaire
        self.current_order = self.next_order
        self.next_order = next_horaire.order
        self.timer.start(remaining_time, self.on_time_out)
        print(F'next timeout in {str(remaining_time)}s')

    def set_order(self, order: Orders):
        self.pilot.set_order(order)

    def set_current_order(self, order: Orders):
        self.current_order = order
        self.set_order(order)

    def get_remaining_time(self):
        return self.timer.get_remaining_time()
