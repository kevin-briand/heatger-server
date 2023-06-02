import unittest

from src.zone.dto.horaire import Horaire


class TestHoraire(unittest.TestCase):
    def test_array_to_horaire(self):
        list_horaire = [{
            "day": 4,
            "hour": "12:00:00",
            "order": 0
        }]
        self.assertEqual(len(Horaire.array_to_horaire(list_horaire)), 1)


if __name__ == '__main__':
    unittest.main()
