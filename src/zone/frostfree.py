import json
from datetime import datetime

from src.localStorage.persistence import Persistence
from src.network.mqtt.homeAssistant.consts import FROSTFREE
from src.shared.enum.orders import Orders
from src.shared.logs.logs import Logs
from src.zone.base import Base
from src.zone.zone import Zone

CLASSNAME = 'Frostfree'


class Frostfree(Base):
    def __init__(self, zones: [Zone]):
        super().__init__()
        Logs.info(CLASSNAME, 'Init...')
        self.zones = zones
        self.end_date = None

    def on_time_out(self):
        self.timer.stop()
        for zone in self.zones:
            Logs.info(zone.id, 'Stop frostfree')
            zone.set_frostfree(False)

    def restore(self):
        persist_date = Persistence().get_value(FROSTFREE)
        if persist_date is not None and persist_date != '':
            self.start(datetime.strptime(persist_date, '%Y-%m-%d %H:%M'))

    def start(self, end_date: datetime):
        remaining_time = end_date.timestamp() - datetime.now().timestamp()
        self.timer.start(remaining_time, self.on_time_out)
        Persistence().set_value(FROSTFREE, end_date.strftime('%Y-%m-%d %H:%M'))
        for zone in self.zones:
            Logs.info(zone.id, 'Start frostfree')
            zone.set_frostfree(True)

    def stop(self):
        self.on_time_out()
        Persistence().set_value(FROSTFREE, '')

    def get_data(self) -> [str]:
        return json.dumps({FROSTFREE: self.timer.get_remaining_time()})

    def set_order(self, order: Orders):
        pass
