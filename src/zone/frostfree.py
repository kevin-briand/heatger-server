"""Frostfree class"""
from datetime import datetime

from src.localStorage.persistence import Persistence
from src.network.mqtt.homeAssistant.consts import FROSTFREE
from src.shared.enum.state import State
from src.shared.logs.logs import Logs
from src.zone.base import Base
from src.zone.dto.info_frostfree import InfoFrostfree
from src.zone.zone import Zone

CLASSNAME = 'Frost free'


class Frostfree(Base):
    """this class manage zone class, stop it if started and resume if stopped or timeout"""
    def __init__(self, zones: [Zone]):
        super().__init__()
        Logs.info(CLASSNAME, 'Init...')
        self.zones = zones
        self.end_date = None
        Logs.info(CLASSNAME, 'Started !')

    def on_time_out(self):
        """called when the timer ended"""
        self.timer.stop()
        for zone in self.zones:
            Logs.info(zone.zone_id, 'Stop frost free')
            zone.set_frostfree(False)

    def restore(self):
        """resume frost-free if device restarted"""
        persist_date = Persistence().get_value(FROSTFREE)
        if persist_date is not None and persist_date != '':
            end_date = datetime.strptime(persist_date, '%Y-%m-%d %H:%M')
            if end_date > datetime.now():
                self.start(end_date)
            else:
                self.stop()

    def start(self, end_date: datetime):
        """Start frost-free with end date"""
        remaining_time = end_date.timestamp() - datetime.now().timestamp()
        self.timer.start(remaining_time, self.stop)
        Persistence().set_value(FROSTFREE, end_date.strftime('%Y-%m-%d %H:%M'))
        self.end_date = end_date
        for zone in self.zones:
            Logs.info(zone.zone_id, 'Start frost free')
            zone.set_frostfree(True)

    def stop(self):
        """stop frost-free"""
        self.on_time_out()
        self.end_date = None
        Persistence().set_value(FROSTFREE, '')

    def get_data(self) -> InfoFrostfree:
        """return remaining time in json object"""
        return InfoFrostfree(self.end_date if self.end_date else None)

    def set_order(self, order: State):
        """unused"""
