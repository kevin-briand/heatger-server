import abc
from datetime import datetime, timedelta

from src.shared.enum.orders import Orders
from src.shared.timer.timer import Timer


class Base(metaclass=abc.ABCMeta):
    def __init__(self):
        super().__init__()
        self.timer = Timer()

    @abc.abstractmethod
    def on_time_out(self):
        raise NotImplementedError

    @abc.abstractmethod
    def set_order(self, order: Orders):
        raise NotImplementedError

    def get_remaining_time(self) -> int:
        return self.timer.get_remaining_time()

    @staticmethod
    def get_next_day(weekday: int, hour: datetime.time) -> datetime:
        now = datetime.now()
        actual_weekday = datetime.now().weekday()
        if actual_weekday > weekday:
            next_day = ((7 - actual_weekday) + weekday)
        elif actual_weekday == weekday and (hour.hour < now.hour or (hour.hour == now.hour and hour.minute < now.minute)):
            next_day = 7
        else:
            next_day = (weekday - actual_weekday)

        td = timedelta(days=next_day)
        result = datetime.fromtimestamp(datetime.now().timestamp() + td.total_seconds())
        return result.replace(hour=hour.hour, minute=hour.minute, second=0, microsecond=0)