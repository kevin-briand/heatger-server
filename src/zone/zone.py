import time

from src.localStorage.config import Config
from src.localStorage.persistence import Persistence
from src.network.ping.ping import Ping
from src.pilot.pilot import Pilot
from src.shared.consts.consts import ENABLED
from src.shared.enum.mode import Mode
from src.shared.enum.orders import Orders
from src.shared.logs.logs import Logs
from src.zone.base import Base
from src.zone.consts import PROG, ZONE, NAME, GPIO_ECO, GPIO_FROSTFREE
from src.zone.dto.horaire import Horaire
from datetime import datetime

from src.zone.dto.infoZone import InfoZone


class Zone(Base):
    def __init__(self, number: int, network=None):
        super().__init__()
        config = Config().get_config()[F"{ZONE}{number}"]
        self.id = F"{ZONE}{number}"
        Logs.info(self.id, 'Init Zone ' + str(number))
        self.name = config[NAME]
        self.current_order = Orders.ECO
        self.current_mode = Mode.AUTO
        self.next_order = Orders.ECO
        self.clock_activated = config[ENABLED]
        self.current_horaire = None
        self.pilot = Pilot(config[GPIO_ECO], config[GPIO_FROSTFREE], True)
        self.network = network
        self.ping = Ping(self.id, self.on_ip_found)
        self.restore_state()

    def restore_state(self):
        persist = Persistence().get_value(self.id)
        if not persist:
            Persistence().set_order(self.id, self.current_order)
            Persistence().set_mode(self.id, self.current_mode)
            return
        self.current_order = Persistence().get_order(self.id)
        mode = Persistence().get_mode(self.id)
        if self.current_mode != mode:
            self.toggle_mode()
        else:
            self.start_next_order()
        current_horaire = self.get_current_and_next_horaire()[0]
        if current_horaire.order == Orders.COMFORT:
            self.set_order(Orders.ECO)
            self.launch_ping()
        else:
            self.set_order(Orders.ECO)

    def on_ip_found(self):
        self.set_order(Orders.COMFORT)

    def on_time_out(self):
        Logs.info(self.id, F'timeout zone {self.name}')
        if self.next_order == Orders.COMFORT:
            self.launch_ping()
        else:
            self.set_order(self.next_order)
        time.sleep(1)
        self.start_next_order()

    def toggle_order(self):
        if self.current_order == Orders.COMFORT:
            self.set_order(Orders.ECO)
        else:
            self.set_order(Orders.COMFORT)

    def launch_ping(self):
        if self.ping.is_running():
            self.ping.stop()
            self.ping.join()
        self.ping = Ping(self.id, self.on_ip_found)
        self.ping.start()

    def set_order(self, order: Orders):
        Logs.info(self.id, F'zone {self.name} switch {self.current_order.name} to {order.name}')
        self.current_order = order
        if order != Orders.FROSTFREE:
            Persistence().set_order(self.id, order)
        self.pilot.set_order(order)

    def toggle_mode(self):
        if self.current_mode == Mode.AUTO:
            self.current_mode = Mode.MANUAL
            self.clock_activated = False
            self.current_horaire = None
            self.timer.stop()
        else:
            self.current_mode = Mode.AUTO
            self.clock_activated = True
        Persistence().set_mode(self.id, self.current_mode)
        Logs.info(self.id, "Mode set to " + self.current_mode.name)
        if self.clock_activated:
            self.restore_state()

    def set_frostfree(self, activate: bool):
        if activate:
            if self.current_mode == Mode.AUTO:
                self.toggle_mode()
            self.current_horaire = None
            self.set_order(Orders.FROSTFREE)
        else:
            if self.current_mode == Mode.MANUAL:
                self.toggle_mode()

    def start_next_order(self):
        if not self.clock_activated or self.current_mode != Mode.AUTO:
            return

        current_horaire, next_horaire = self.get_current_and_next_horaire()
        horaire_date: datetime
        now = datetime.now()

        horaire_date = Zone.get_next_day(next_horaire.day, next_horaire.hour)
        remaining_time = int(horaire_date.timestamp() - now.timestamp())

        self.current_horaire = current_horaire
        self.next_order = next_horaire.order
        self.timer.start(remaining_time, self.on_time_out)
        Logs.info(self.id, F'next timeout in {str(remaining_time)}s')

    def get_current_and_next_horaire(self) -> [Horaire, Horaire]:
        config = Config().get_config().get(self.id)
        list_horaires = Horaire.array_to_horaire(config[PROG])
        if list_horaires is None or len(list_horaires) == 0:
            Logs.error(self.id, "horaire list is empty")
            return [None, None]
        current_horaire: Horaire or None = None
        next_horaire: Horaire or None = None
        horaire_date: datetime
        now = datetime.now()

        for horaire in list_horaires:
            horaire_date = Zone.get_next_day(horaire.day, horaire.hour)
            if horaire_date > now and horaire is not self.current_horaire:
                if next_horaire is None or horaire_date < Zone.get_next_day(next_horaire.day, next_horaire.hour):
                    next_horaire = horaire
            if horaire_date <= now and (
                    current_horaire is None or
                    horaire_date > Zone.get_next_day(current_horaire.day, current_horaire.hour) < horaire_date):
                current_horaire = horaire

        if current_horaire is None:
            current_horaire = list_horaires[len(list_horaires) - 1]
        if next_horaire is None:
            next_horaire = list_horaires[0]
        return [current_horaire, next_horaire]

    def get_data(self) -> InfoZone:
        next_change = datetime.fromtimestamp(datetime.now().timestamp() + self.get_remaining_time())
        if self.get_remaining_time() == -1:
            next_change = 'Never'

        return InfoZone(self.id,
                        self.name,
                        self.current_order,
                        next_change,
                        self.get_remaining_time(),
                        self.current_mode).to_json()
