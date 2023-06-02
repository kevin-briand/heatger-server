"""Test Ping class"""
import unittest

from src.network.ping.ping import Ping


class TestPing(unittest.TestCase):
    """Test Ping class"""
    def test_get_ip(self):
        """Test get_ip func"""
        self.assertEqual(len(Ping.get_ip().split('.')), 4)

    def test_is_valid_ip(self):
        """Test is_valid_ip func"""
        self.assertEqual(Ping.is_valid_ip('127.0.0.1'),  True)
        self.assertEqual(Ping.is_valid_ip('127.0.0'),  False)


if __name__ == '__main__':
    unittest.main()
