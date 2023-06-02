"""Test Mode enum"""
import unittest

from src.shared.enum.mode import Mode


class TestMode(unittest.TestCase):
    """Test Mode enum"""
    def test_to_mode(self):
        """Test to_mode func"""
        self.assertEqual(Mode.to_mode(0), Mode.AUTO)


if __name__ == '__main__':
    unittest.main()
