import json
from unittest.mock import patch, mock_open

from src.localStorage.jsonEncoder.json_encoder import JsonEncoder


class LocalStoragePatch:
    _datas = None

    @classmethod
    def start_patch(cls, test):
        test.open_file = patch('src.localStorage.local_storage.open', cls.__mock_open_file())
        test.open_file.start()
        test.remove_file = patch('os.remove')
        test.remove_file.start()

    @classmethod
    def stop_patch(cls, test):
        test.open_file.stop()
        test.remove_file.stop()

    @classmethod
    def __mock_open_file(cls):
        mock_open_obj = mock_open()
        mock_file_handle = mock_open_obj.return_value
        mock_file_handle.read.return_value = cls._read_data()
        mock_file_handle.write.side_effect = cls.__write_data
        return mock_open_obj

    @classmethod
    def _read_data(cls):
        return json.dumps(cls._datas, cls=JsonEncoder)

    @classmethod
    def __write_data(cls, data):
        cls._datas = data
