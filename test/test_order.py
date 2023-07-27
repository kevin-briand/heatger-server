"""Test Orders enum"""
import unittest

from src.shared.enum.state import State


class TestOrders(unittest.TestCase):
    """Test Orders enum"""
    def test_to_order(self):
        """Test to_order func"""
        self.assertEqual(State.to_state(0), State.COMFORT)


if __name__ == '__main__':
    unittest.main()
