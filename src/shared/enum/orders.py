from enum import Enum


class Orders(Enum):
    COMFORT = 0
    ECO = 1
    FROSTFREE = 2

    @staticmethod
    def to_order(zone: int):
        if zone == Orders.COMFORT.value:
            return Orders.COMFORT
        elif zone == Orders.ECO.value:
            return Orders.ECO
        else:
            return Orders.FROSTFREE

