"""Test HoraireDto class"""
import unittest

from src.zone.dto.horaire_dto import HoraireDto


class TestHoraireDto(unittest.TestCase):
    """Test HoraireDto class"""
    def test_array_to_horaire(self):
        """Test array_to_horaire func"""
        list_horaire = [{
            "day": 4,
            "hour": "12:00:00",
            "order": 0
        }]
        self.assertEqual(len(HoraireDto.array_to_horaire(list_horaire)), 1)


if __name__ == '__main__':
    unittest.main()
