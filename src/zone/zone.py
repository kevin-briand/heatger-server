from array import array

from src.localStorage.config import Config
from src.network.mqtt.homeAssistant.consts import PUBLISH_DATA_SENSOR
from src.pilot.pilot import Pilot
from src.shared.consts.consts import ENABLED
from src.shared.enum.orders import Orders
from src.shared.message.message import info
from src.shared.timer.timer import Timer
from src.zone.consts import PROG, ZONE, NAME, GPIO_ECO, GPIO_FROSTFREE, CLASSNAME
from src.zone.dto.horaire import Horaire
from datetime import datetime, timedelta

from src.zone.dto.infoZone import InfoZone


class Zone:
    def __init__(self, number: int, network=None):
        info(CLASSNAME, 'Init Zone ' + str(number))
        config = Config().get_config()[F"{ZONE}{number}"]
        self.id = F"{ZONE}{number}"
        self.name = config[NAME]
        self.timer = Timer()
        self.current_order = Orders.COMFORT
        self.next_order = Orders.ECO
        self.clock_activated = config[ENABLED]
        self.list_horaires = Horaire.array_to_horaire(config[PROG])
        self.current_horaire = None
        self.pilot = Pilot(config[GPIO_ECO], config[GPIO_FROSTFREE], True)
        self.network = network
        if self.clock_activated and len(self.list_horaires) != 0:
            self.start_next_order()

    def set_list_horaires(self, list_horaires):
        self.list_horaires: array = list_horaires
        if self.clock_activated and list_horaires is not None:
            self.start_next_order()

    def on_time_out(self):
        info(CLASSNAME, F'timeOut zone {self.name} switch {self.current_order.name} to {self.next_order.name}')
        info(CLASSNAME, 'starting ping...')
        self.network.scan()
        self.set_order(self.next_order)
        self.start_next_order()

    def start_next_order(self):
        next_horaire: Horaire = None
        remaining_time: int = 0
        horaire_date: datetime
        now = datetime.now()
        for horaire in self.list_horaires:
            horaire_date = Zone.get_next_day(horaire.day, horaire.hour)
            if horaire_date > datetime.now() and horaire is not self.current_horaire:
                if next_horaire is None or horaire_date < Zone.get_next_day(next_horaire.day, next_horaire.hour):
                    next_horaire = horaire
                    remaining_time = int(horaire_date.timestamp() - now.timestamp())

        if next_horaire is None:
            if len(self.list_horaires) > 0:
                horaire_date = Zone.get_next_day(self.list_horaires[0].day, self.list_horaires[0].hour)
                next_horaire = self.list_horaires[0]
                remaining_time = int(horaire_date.timestamp() - now.timestamp())
            else:
                return

        self.current_horaire = next_horaire
        self.current_order = self.next_order
        self.next_order = next_horaire.order
        self.timer.start(remaining_time, self.on_time_out)
        self.update_mqtt_data()
        info(CLASSNAME, F'next timeout in {str(remaining_time)}s')

    def set_order(self, order: Orders):
        self.pilot.set_order(order)

    def update_mqtt_data(self):
        self.network.mqtt.publish_data(PUBLISH_DATA_SENSOR, InfoZone(self.id,
                                                                     self.name,
                                                                     self.current_order.name,
                                                                     datetime.fromtimestamp(datetime.now().timestamp() +
                                                                                            self.get_remaining_time()),
                                                                     self.get_remaining_time()).to_json())

    def set_current_order(self, order: Orders):
        self.current_order = order
        self.set_order(order)

    def get_remaining_time(self):
        return self.timer.get_remaining_time()

    @staticmethod
    def get_next_day(weekday: int, hour: datetime.time) -> datetime:
        now = datetime.now()
        actual_weekday = datetime.now().weekday()
        if actual_weekday > weekday:
            next_day = ((7 - actual_weekday) + weekday)
        elif actual_weekday == weekday and (hour.hour < now.hour or (hour.hour == now.hour and hour.minute < now.minute)):
            next_day = 7
        else:
            next_day = (weekday - actual_weekday)

        td = timedelta(days=next_day)
        result = datetime.fromtimestamp(datetime.now().timestamp() + td.total_seconds())
        return result.replace(hour=hour.hour, minute=hour.minute, second=0, microsecond=0)
