import unittest

from src.network.ping.ping import Ping


class TestPing(unittest.TestCase):

    def test_get_ip(self):
        ip = Ping.get_ip()
        self.assertEqual(len(ip.split('.')), 4)

    def test_is_valid_ip(self):
        self.assertEqual(Ping.is_valid_ip('127.0.0.1'),  True)
        self.assertEqual(Ping.is_valid_ip('127.0.0'),  False)


if __name__ == '__main__':
    unittest.main()
