"""Test Orders enum"""
import unittest

from src.shared.enum.orders import Orders


class TestOrders(unittest.TestCase):
    """Test Orders enum"""
    def test_to_order(self):
        """Test to_order func"""
        self.assertEqual(Orders.to_order(0), Orders.COMFORT)


if __name__ == '__main__':
    unittest.main()
