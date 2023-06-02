"""Orders enum"""
from enum import Enum


class Orders(Enum):
    """Orders enum"""
    COMFORT = 0
    ECO = 1
    FROSTFREE = 2

    @staticmethod
    def to_order(order_num: int):
        """return Order corresponding of number given"""
        if order_num == Orders.COMFORT.value:
            return Orders.COMFORT
        if order_num == Orders.ECO.value:
            return Orders.ECO
        return Orders.FROSTFREE
