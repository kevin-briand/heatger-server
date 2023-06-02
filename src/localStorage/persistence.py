"""Persistence class"""
from src.localStorage.consts import CURRENT_ORDER, CURRENT_MODE
from src.localStorage.local_storage import LocalStorage
from src.shared.enum.mode import Mode
from src.shared.enum.orders import Orders

CLASSNAME = 'Persistence'


class Persistence(LocalStorage):
    """Load/Save Heatger state in file"""
    def __init__(self):
        super().__init__('persist.json')
        self.persist = self.read()

    def get_value(self, key: str):
        """return value of key"""
        return self.persist.get(key)

    def set_value(self, key: str, value: str):
        """write value to file"""
        self.persist[key] = value
        self.write(self.persist)

    def set_order(self, zone_id: str, order: Orders):
        """write order in file"""
        zone = self.persist.get(zone_id)
        if zone is None:
            zone = {}
        zone[CURRENT_ORDER] = order.value
        self.set_value(zone_id, zone)

    def set_mode(self, zone_id: str, mode: Mode):
        """write mode in file"""
        zone = self.persist.get(zone_id)
        if zone is None:
            zone = {}
        zone[CURRENT_MODE] = mode.value
        self.set_value(zone_id, zone)

    def get_order(self, zone_id: str) -> Orders:
        """get order in file"""
        zone = self.persist.get(zone_id)
        if zone:
            return Orders.to_order(zone.get(CURRENT_ORDER))
        return Orders.COMFORT

    def get_mode(self, zone_id: str) -> Mode:
        """get mode in file"""
        zone = self.persist.get(zone_id)
        if zone:
            return Mode.to_mode(zone.get(CURRENT_MODE))
        return Mode.AUTO
