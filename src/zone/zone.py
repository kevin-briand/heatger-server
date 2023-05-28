from src.localStorage.config import Config
from src.localStorage.persistence import Persistence
from src.pilot.pilot import Pilot
from src.shared.consts.consts import ENABLED
from src.shared.enum.mode import Mode
from src.shared.enum.orders import Orders
from src.shared.logs.logs import Logs
from src.shared.timer.timer import Timer
from src.zone.consts import PROG, ZONE, NAME, GPIO_ECO, GPIO_FROSTFREE
from src.zone.dto.horaire import Horaire
from datetime import datetime, timedelta

from src.zone.dto.infoZone import InfoZone


class Zone:
    def __init__(self, number: int, network=None):
        config = Config().get_config()[F"{ZONE}{number}"]
        self.id = F"{ZONE}{number}"
        Logs.info(self.id, 'Init Zone ' + str(number))
        self.name = config[NAME]
        self.timer = Timer()
        self.current_order = Orders.COMFORT
        self.current_mode = Mode.AUTO
        self.next_order = Orders.ECO
        self.clock_activated = config[ENABLED]
        self.current_horaire = None
        self.pilot = Pilot(config[GPIO_ECO], config[GPIO_FROSTFREE], True)
        self.network = network
        self.restore_state()
        self.start_next_order()

    def restore_state(self):
        persist = Persistence().get_value(self.id)
        if not persist:
            Persistence().set_order(self.id, self.current_order)
            Persistence().set_mode(self.id, self.current_mode)
            return
        self.current_order = Persistence().get_order(self.id)
        mode = Persistence().get_mode(self.id)
        self.set_order(self.current_order)
        if self.current_mode != mode:
            self.toggle_mode()

    def on_time_out(self):
        Logs.info(self.id, F'timeOut zone {self.name}')
        Logs.info(self.id, 'starting ping...')
        self.network.scan_ips_list()
        self.set_order(self.next_order)
        self.start_next_order()

    def toggle_order(self):
        if self.current_order == Orders.COMFORT:
            self.set_order(Orders.ECO)
        else:
            self.set_order(Orders.COMFORT)

    def toggle_mode(self):
        if self.current_mode == Mode.AUTO:
            self.current_mode = Mode.MANUAL
            self.clock_activated = False
            self.timer.stop()
        else:
            self.current_mode = Mode.AUTO
            self.clock_activated = True
            self.start_next_order()
        Persistence().set_mode(self.id, self.current_mode)
        Logs.info(self.id, "Mode set to " + self.current_mode.name)

    def start_next_order(self):
        if not self.clock_activated or self.current_mode != Mode.AUTO:
            return
        next_horaire: Horaire = None
        remaining_time: int = 0
        horaire_date: datetime
        now = datetime.now()
        config = Config().get_config().get(self.id)
        list_horaires = Horaire.array_to_horaire(config[PROG])
        for horaire in list_horaires:
            horaire_date = Zone.get_next_day(horaire.day, horaire.hour)
            if horaire_date > datetime.now() and horaire is not self.current_horaire:
                if next_horaire is None or horaire_date < Zone.get_next_day(next_horaire.day, next_horaire.hour):
                    next_horaire = horaire
                    remaining_time = int(horaire_date.timestamp() - now.timestamp())

        if next_horaire is None:
            if len(list_horaires) > 0:
                horaire_date = Zone.get_next_day(list_horaires[0].day, list_horaires[0].hour)
                next_horaire = list_horaires[0]
                remaining_time = int(horaire_date.timestamp() - now.timestamp())
            else:
                return

        self.current_horaire = next_horaire
        self.next_order = next_horaire.order
        if self.next_order == self.current_order:
            self.toggle_order()
        self.timer.start(remaining_time, self.on_time_out)
        Logs.info(self.id, F'next timeout in {str(remaining_time)}s')

    def set_order(self, order: Orders):
        Logs.info(self.id, F'zone {self.name} switch {self.current_order.name} to {order.name}')
        self.current_order = order
        Persistence().set_order(self.id, order)
        self.pilot.set_order(order)

    def get_data(self):
        next_change = datetime.fromtimestamp(datetime.now().timestamp() + self.get_remaining_time())
        if self.get_remaining_time() == -1:
            next_change = 'Never'

        return InfoZone(self.id,
                        self.name,
                        self.current_order.name,
                        next_change,
                        self.get_remaining_time(),
                        self.current_mode.name).to_json()

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
