import json
import os
import unittest
from unittest.mock import patch, mock_open

from src.localStorage.errors.file_not_readable_error import FileNotReadableError
from src.localStorage.errors.file_not_writable_error import FileNotWritableError
from src.localStorage.local_storage import LocalStorage
from src.shared.errors.file_empty_error import FileEmptyError
from src.shared.timer.timer import Timer


class TestLocalStorage(unittest.TestCase):
    config_datas: str = None

    def setUp(self) -> None:
        self.filename = "test.txt"
        self.path = os.path.dirname(__file__).split('test')[0]
        self.data = {"test": "True"}

    def tearDown(self) -> None:
        if os.path.isfile(self.path + self.filename):
            os.remove(self.path + self.filename)

    def create_file_with_data(self):
        with open(self.path + self.filename, 'w', encoding='utf-8') as file:
            file.write(json.dumps(self.data))

    @staticmethod
    def mock_open_file():
        mock_open_obj = mock_open()
        mock_file_handle = mock_open_obj.return_value
        mock_file_handle.readable.return_value = False
        mock_file_handle.writable.return_value = False
        return mock_open_obj

    def stop_is_write(self):
        self.local_storage.is_write = False

    def test_create_file_if_not_exist(self):
        self.assertFalse(os.path.isfile(self.path + self.filename))

        self.local_storage = LocalStorage(self.filename)

        self.assertTrue(os.path.isfile(self.path + self.filename))

    def test_do_nothing_if_file_already_exist(self):
        self.assertFalse(os.path.isfile(self.path + self.filename))

        self.local_storage = LocalStorage(self.filename)
        self.assertTrue(os.path.isfile(self.path + self.filename))

        self.local_storage = LocalStorage(self.filename)
        self.assertTrue(os.path.isfile(self.path + self.filename))

    def test_read_file(self):
        self.create_file_with_data()
        self.local_storage = LocalStorage(self.filename)

        result = self.local_storage._read()

        self.assertEqual(result, self.data)

    def test_read_file_wait_if_write_in_progress(self):
        self.create_file_with_data()
        self.local_storage = LocalStorage(self.filename)
        self.local_storage.is_write = True
        timer = Timer()
        timer.start(1, self.stop_is_write)

        result = self.local_storage._read()

        self.assertLessEqual(timer.get_remaining_time(), 0)
        self.assertEqual(result, self.data)

    def test_read_file_should_throw_error_if_not_readable(self):
        with patch('src.localStorage.local_storage.open', self.mock_open_file()):
            with self.assertRaises(FileNotReadableError):
                self.local_storage = LocalStorage(self.filename)
                self.local_storage._read()

    def test_read_file_should_throw_error_if_file_is_empty(self):
        self.local_storage = LocalStorage(self.filename)

        with self.assertRaises(FileEmptyError):
            self.local_storage._read()

    def test_write_file(self):
        self.create_file_with_data()
        self.local_storage = LocalStorage(self.filename)
        new_data = {'test2': 'False'}
        new_data.update(self.data)

        self.local_storage._write(new_data)

        self.assertEqual(self.local_storage._read(), new_data)

    def test_write_file_should_throw_error_if_not_writable(self):
        self.create_file_with_data()
        self.local_storage = LocalStorage(self.filename)
        new_data = {'test2': 'False'}
        new_data.update(self.data)

        with patch('src.localStorage.local_storage.open', self.mock_open_file()):
            with self.assertRaises(FileNotWritableError):
                self.local_storage = LocalStorage(self.filename)
                self.local_storage._write(new_data)


if __name__ == '__main__':
    unittest.main()
