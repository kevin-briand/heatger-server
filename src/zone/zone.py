"""Zone class"""
import re
import time

from datetime import datetime
from typing import Optional

from src.localStorage.config.config import Config
from src.localStorage.persistence.persistence import Persistence
from src.network.ping.ping import Ping
from src.pilot.pilot import Pilot
from src.shared.enum.mode import Mode
from src.shared.enum.state import State
from src.shared.logs.logs import Logs
from src.zone.base import Base
from src.zone.consts import ZONE, REGEX_FIND_NUMBER, WAIT_TIME

from src.zone.dto.schedule_dto import ScheduleDto
from src.zone.dto.info_zone import InfoZone


class Zone(Base):
    """This class define a new heaters zone"""

    def __init__(self, number: int):
        super().__init__()
        config = Config().get_zone(F"{ZONE}{number}")
        self.zone_id = F"{ZONE}{number}"
        self.name = config.name
        self.current_state = State.ECO
        self.current_mode = Mode.AUTO
        self.next_state = State.ECO
        self.current_schedule = None
        self.pilot = Pilot(config.gpio_eco, config.gpio_frostfree, True)
        self.ping = Ping(self.zone_id, self.on_ip_found)
        self.is_ping = False
        self.restore_state()

    def restore_state(self) -> None:
        """Restore state/mode after a device reboot"""
        self.current_state = Persistence().get_state(self.zone_id)
        mode = Persistence().get_mode(self.zone_id)
        if self.current_mode != mode:
            self.toggle_mode()
        else:
            self.start_next_state()

        current_schedule = self.get_current_and_next_schedule()[0]
        if current_schedule is None:
            return

        self.set_state(State.ECO)
        if current_schedule.state == State.COMFORT:
            self.launch_ping()

    def toggle_mode(self) -> None:
        """Switch mode Auto <> Manual"""
        if self.current_mode == Mode.AUTO:
            self.current_mode = Mode.MANUAL
            self.current_schedule = None
            self.timer.stop()
            self.is_ping = False
        else:
            self.current_mode = Mode.AUTO
            self.start_next_state()
        Persistence().set_mode(self.zone_id, self.current_mode)
        Logs.info(self.zone_id, "Mode set to " + self.current_mode.name)
        if self.current_mode == Mode.AUTO:
            self.restore_state()

    def start_next_state(self) -> None:
        """Launch next timer (mode Auto)"""
        if self.current_mode != Mode.AUTO:
            return
        current_schedule, next_schedule = self.get_current_and_next_schedule()
        if current_schedule is None or next_schedule is None:
            return

        remaining_time = self.get_remaining_time_from_schedule(next_schedule)

        self.current_schedule = current_schedule
        self.next_state = next_schedule.state
        self.timer.start(remaining_time, self.on_time_out)
        Logs.info(self.zone_id, F'next timeout in {str(remaining_time)}s')

    def get_current_and_next_schedule(self) -> list[Optional[ScheduleDto], Optional[ScheduleDto]]:
        """get the current and next schedule in prog list"""
        zone_config = Config().get_zone(self.zone_id)
        list_schedules = zone_config.prog
        if list_schedules is None or len(list_schedules) == 0:
            return [None, None]

        current_schedule: Optional[ScheduleDto] = None
        next_schedule: Optional[ScheduleDto] = None
        now = datetime.now()

        for schedule in list_schedules:
            schedule_date = Zone.get_next_day(schedule.day, schedule.hour)
            if schedule_date > now and schedule is not self.current_schedule:
                if next_schedule is None or schedule_date < Zone.get_next_day(next_schedule.day, next_schedule.hour):
                    next_schedule = schedule

            if schedule_date <= now and (
                    current_schedule is None or
                    schedule_date > Zone.get_next_day(current_schedule.day, current_schedule.hour)):
                current_schedule = schedule

        if current_schedule is None:
            current_schedule = list_schedules[len(list_schedules) - 1]
        if next_schedule is None:
            next_schedule = list_schedules[0]
        return [current_schedule, next_schedule]

    @staticmethod
    def get_remaining_time_from_schedule(schedule: ScheduleDto) -> int:
        """Return the remaining time between the next schedule and now"""
        schedule_date = Zone.get_next_day(schedule.day, schedule.hour)
        return int(schedule_date.timestamp() - datetime.now().timestamp())

    def launch_ping(self) -> None:
        """Start discovery ip on network"""
        self.is_ping = True
        if self.ping.is_running():
            self.ping.stop()
            self.ping.join()
        self.ping = Ping(self.zone_id, self.on_ip_found)
        self.ping.start()

    def set_state(self, state: State) -> None:
        """change state"""
        Logs.info(self.zone_id, F'zone {self.name} switch {self.current_state.name} to {state.name}')
        self.current_state = state
        if state != State.FROSTFREE:
            Persistence().set_state(self.zone_id, state)
        self.pilot.set_state(state)

    def on_ip_found(self) -> None:
        """Called when ip found on network(Ping class)"""
        if not self.is_ping:
            return
        self.is_ping = False
        self.set_state(State.COMFORT)

    def on_time_out(self) -> None:
        """Called when timeout fired"""
        Logs.info(self.zone_id, F'timeout zone {self.name}')
        if self.next_state == State.COMFORT:
            self.launch_ping()
        else:
            self.set_state(self.next_state)
            self.ping.stop()
            self.is_ping = False
        time.sleep(WAIT_TIME)  # wait 1sec before start next timer to avoid a loop
        self.start_next_state()

    def toggle_state(self) -> None:
        """Switch state Comfort <> Eco"""
        if self.current_state == State.COMFORT:
            self.set_state(State.ECO)
        else:
            self.set_state(State.COMFORT)

    def set_frostfree(self, activate: bool) -> None:
        """Activate/deactivate frost-free"""
        if activate:
            if self.current_mode == Mode.AUTO:
                self.toggle_mode()
            self.current_schedule = None
            self.ping.stop()
            self.is_ping = False
            self.set_state(State.FROSTFREE)
        elif self.current_mode == Mode.MANUAL:
            self.toggle_mode()

    def get_data(self) -> InfoZone:
        """return information zone in json object"""
        next_change = datetime.fromtimestamp(datetime.now().timestamp() + self.get_remaining_time())
        if self.get_remaining_time() == -1:
            next_change = None

        return InfoZone(self.zone_id,
                        self.name,
                        self.current_state,
                        next_change,
                        self.is_ping,
                        self.current_mode)

    @staticmethod
    def get_zone_number(topic: str) -> int:
        """Return the zone number, else -1"""
        zone_number = re.search(REGEX_FIND_NUMBER, topic)
        if zone_number is None:
            return -1
        return int(zone_number.group(0))
