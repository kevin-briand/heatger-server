"""Test base class"""
import unittest
from datetime import datetime, timedelta

from src.zone.base import Base


class TestBase(unittest.TestCase):
    """Test base class"""

    @staticmethod
    def get_shifted_date_from_now(days: int) -> datetime:
        now = datetime.now()
        delta = timedelta(days=days)
        shifted_date = datetime.fromtimestamp(now.timestamp() + delta.total_seconds())
        return shifted_date.replace(hour=now.hour, minute=now.minute, second=0, microsecond=0)

    def test_get_next_day(self):
        """Test get_next_day func"""
        now = datetime.now()
        # should return current day
        self.assertEqual(Base.get_next_day(now.weekday(), now.time()), self.get_shifted_date_from_now(0))
        # should return next day
        self.assertEqual(Base.get_next_day(now.weekday()+1, now.time()), self.get_shifted_date_from_now(1))
        # should return day + 6
        self.assertEqual(Base.get_next_day(now.weekday()-1, now.time()), self.get_shifted_date_from_now(6))
        # should return day + 7
        past_hour = now.replace(hour=now.hour-1)
        self.assertEqual(Base.get_next_day(now.weekday(), past_hour),
                         self.get_shifted_date_from_now(7).replace(hour=now.hour-1))


if __name__ == '__main__':
    unittest.main()
