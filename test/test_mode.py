"""Test Mode enum"""
import unittest

from src.shared.enum.mode import Mode


class TestMode(unittest.TestCase):
    def test_to_mode(self):
        self.assertEqual(Mode.to_mode(0), Mode.AUTO)

    def test_unknown_mode(self):
        self.assertEqual(Mode.to_mode(10), Mode.MANUAL)


if __name__ == '__main__':
    unittest.main()
