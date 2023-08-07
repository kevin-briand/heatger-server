"""Test ScheduleDto class"""
import unittest

from src.zone.dto.schedule_dto import ScheduleDto


class TestScheduleDto(unittest.TestCase):
    """Test ScheduleDto class"""
    def test_array_to_schedule(self):
        """Test array_to_horaire func"""
        list_schedule = [{
            "day": 4,
            "hour": "12:00:00",
            "state": 0
        }]
        self.assertEqual(len(ScheduleDto.from_array(list_schedule)), 1)


if __name__ == '__main__':
    unittest.main()
