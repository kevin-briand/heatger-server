from enum import Enum


class Orders(Enum):
    COMFORT = 0
    ECO = 1
    FROSTFREE = 2

    @staticmethod
    def to_order(order_num: int):
        if order_num == Orders.COMFORT.value:
            return Orders.COMFORT
        elif order_num == Orders.ECO.value:
            return Orders.ECO
        else:
            return Orders.FROSTFREE

