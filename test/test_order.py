"""Test Orders enum"""
import unittest

from src.shared.enum.state import State


class TestOrders(unittest.TestCase):
    def test_to_state(self):
        self.assertEqual(State.to_state(0), State.COMFORT)

    def test_unknown_state(self):
        self.assertEqual(State.to_state(10), State.FROSTFREE)


if __name__ == '__main__':
    unittest.main()
