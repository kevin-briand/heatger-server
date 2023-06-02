import unittest
from datetime import datetime

from src.zone.base import Base


class TestBase(unittest.TestCase):
    def test_get_next_day(self):
        now = datetime.now()
        # should return current day
        self.assertEqual(Base.get_next_day(now.weekday(), now.time()), datetime(now.year, now.month, now.day, now.hour, now.minute, 0, 0))
        # should return next day
        self.assertEqual(Base.get_next_day(now.weekday()+1, now.time()), datetime(now.year, now.month, now.day+1, now.hour, now.minute, 0, 0))
        # should return day + 6
        self.assertEqual(Base.get_next_day(now.weekday()-1, now.time()), datetime(now.year, now.month, now.day+6, now.hour, now.minute, 0, 0))
        past_hour = now.replace(hour=now.hour-1)
        # should return day + 7
        self.assertEqual(Base.get_next_day(now.weekday(), past_hour), datetime(now.year, now.month, now.day+7, now.hour-1, now.minute, 0, 0))


if __name__ == '__main__':
    unittest.main()
