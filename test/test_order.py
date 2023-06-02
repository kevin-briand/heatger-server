import unittest

from src.shared.enum.orders import Orders


class TestOrders(unittest.TestCase):
    def test_to_order(self):
        self.assertEqual(Orders.to_order(0), Orders.COMFORT)


if __name__ == '__main__':
    unittest.main()
