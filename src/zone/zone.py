"""Zone class"""
import re
import time

from datetime import datetime
from src.localStorage.config import Config
from src.localStorage.persistence import Persistence
from src.network.ping.ping import Ping
from src.pilot.pilot import Pilot
from src.shared.enum.mode import Mode
from src.shared.enum.orders import Orders
from src.shared.logs.logs import Logs
from src.zone.base import Base
from src.zone.consts import ZONE

from src.zone.dto.horaire_dto import HoraireDto
from src.zone.dto.info_zone import InfoZone


class Zone(Base):
    """This class define a new heaters zone"""
    def __init__(self, number: int, network=None):
        super().__init__()
        config = getattr(Config().get_config(), F"{ZONE}{number}")
        self.zone_id = F"{ZONE}{number}"
        Logs.info(self.zone_id, 'Init Zone ' + str(number))
        self.name = config.name
        self.current_order = Orders.ECO
        self.current_mode = Mode.AUTO
        self.next_order = Orders.ECO
        self.clock_activated = config.enabled
        self.current_horaire = None
        self.pilot = Pilot(config.gpio_eco, config.gpio_frostfree, True)
        self.network = network
        self.ping = Ping(self.zone_id, self.on_ip_found)
        self.is_ping = False
        self.restore_state()
        Logs.info(self.zone_id, 'Started !')

    def restore_state(self):
        """Restore state/mode after a device reboot"""
        persist = Persistence().get_value(self.zone_id)
        if not persist:
            Persistence().set_order(self.zone_id, self.current_order)
            Persistence().set_mode(self.zone_id, self.current_mode)
            return
        self.current_order = Persistence().get_order(self.zone_id)
        mode = Persistence().get_mode(self.zone_id)
        if self.current_mode != mode:
            self.toggle_mode()
        else:
            self.start_next_order()
        current_horaire = self.get_current_and_next_horaire()[0]
        if current_horaire is None:
            return
        if current_horaire.order == Orders.COMFORT:
            self.set_order(Orders.ECO)
            self.launch_ping()
        else:
            self.set_order(Orders.ECO)

    def on_ip_found(self):
        """Called when ip found on network(Ping class)"""
        if not self.is_ping:
            return
        self.is_ping = False
        self.set_order(Orders.COMFORT)

    def on_time_out(self):
        """Called when timeout fired"""
        Logs.info(self.zone_id, F'timeout zone {self.name}')
        if self.next_order == Orders.COMFORT:
            self.launch_ping()
        else:
            self.set_order(self.next_order)
            self.ping.stop()
            self.is_ping = False
        time.sleep(1)
        self.start_next_order()

    def toggle_order(self):
        """Switch state Comfort <> Eco"""
        if self.current_order == Orders.COMFORT:
            self.set_order(Orders.ECO)
        else:
            self.set_order(Orders.COMFORT)

    def launch_ping(self):
        """Start discovery ip on network"""
        self.is_ping = True
        if self.ping.is_running():
            self.ping.stop()
            self.ping.join()
        self.ping = Ping(self.zone_id, self.on_ip_found)
        self.ping.start()

    def set_order(self, order: Orders):
        """change state"""
        Logs.info(self.zone_id,
                  F'zone {self.name} switch {self.current_order.name} to {order.name}')
        self.current_order = order
        if order != Orders.FROSTFREE:
            Persistence().set_order(self.zone_id, order)
        self.pilot.set_order(order)

    def toggle_mode(self):
        """Switch mode Auto <> Manual"""
        if self.current_mode == Mode.AUTO:
            self.current_mode = Mode.MANUAL
            self.clock_activated = False
            self.current_horaire = None
            self.timer.stop()
            self.is_ping = False
        else:
            self.current_mode = Mode.AUTO
            self.clock_activated = True
        Persistence().set_mode(self.zone_id, self.current_mode)
        Logs.info(self.zone_id, "Mode set to " + self.current_mode.name)
        if self.clock_activated:
            self.restore_state()

    def set_frostfree(self, activate: bool):
        """Activate/deactivate frost-free"""
        if activate:
            if self.current_mode == Mode.AUTO:
                self.toggle_mode()
            self.current_horaire = None
            self.ping.stop()
            self.is_ping = False
            self.set_order(Orders.FROSTFREE)
        else:
            if self.current_mode == Mode.MANUAL:
                self.toggle_mode()

    def start_next_order(self):
        """Launch next timer (mode Auto)"""
        if not self.clock_activated or self.current_mode != Mode.AUTO:
            return

        current_horaire, next_horaire = self.get_current_and_next_horaire()
        if current_horaire is None or next_horaire is None:
            return

        horaire_date: datetime
        now = datetime.now()

        horaire_date = Zone.get_next_day(next_horaire.day, next_horaire.hour)
        remaining_time = int(horaire_date.timestamp() - now.timestamp())

        self.current_horaire = current_horaire
        self.next_order = next_horaire.order
        self.timer.start(remaining_time, self.on_time_out)
        Logs.info(self.zone_id, F'next timeout in {str(remaining_time)}s')

    def get_current_and_next_horaire(self) -> [HoraireDto, HoraireDto]:
        """get the current and next horaire in prog list"""
        config = getattr(Config().get_config(), self.zone_id)
        list_horaires = config.prog
        if list_horaires is None or len(list_horaires) == 0:
            Logs.error(self.zone_id, "horaire list is empty")
            return [None, None]
        current_horaire: HoraireDto or None = None
        next_horaire: HoraireDto or None = None
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
        """return information zone in json object"""
        next_change = datetime.fromtimestamp(datetime.now().timestamp() + self.get_remaining_time())
        if self.get_remaining_time() == -1:
            next_change = None

        return InfoZone(self.zone_id,
                        self.name,
                        self.current_order,
                        next_change,
                        self.is_ping,
                        self.current_mode)

    @staticmethod
    def get_zone_number(topic: str) -> int:
        """Return the zone number, else -1"""
        zone_number = re.search(r"\d", topic)
        if zone_number is None:
            return -1
        return int(zone_number.group(0))-1
