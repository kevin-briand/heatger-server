"""Frostfree class"""
from datetime import datetime
from typing import Optional

from src.localStorage.persistence.persistence import Persistence
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
        self.end_date: Optional[datetime] = None
        self.restore()
        Logs.info(CLASSNAME, 'Started !')

    def restore(self) -> None:
        """resume frost-free if device restarted"""
        end_date = Persistence().get_frostfree_end_date()
        if end_date and end_date > datetime.now():
            self.start(end_date)
        else:
            self.stop()

    def on_time_out(self) -> None:
        """called when the timer ended"""
        self.timer.stop()
        for zone in self.zones:
            Logs.info(zone.zone_id, 'Stop frost free')
            zone.set_frostfree(False)

    def start(self, end_date: datetime) -> None:
        """Start frost-free with end date"""
        remaining_time = end_date.timestamp() - datetime.now().timestamp()
        self.timer.start(remaining_time, self.stop)
        Persistence().set_frostfree_end_date(end_date)
        self.end_date = end_date
        for zone in self.zones:
            Logs.info(zone.zone_id, 'Start frost free')
            zone.set_frostfree(True)

    def stop(self) -> None:
        """stop frost-free"""
        self.on_time_out()
        self.end_date = None
        Persistence().set_frostfree_end_date()

    def get_data(self) -> InfoFrostfree:
        """return remaining time in json object"""
        return InfoFrostfree(self.end_date if self.end_date else None)
