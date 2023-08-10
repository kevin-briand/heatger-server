"""LocalStorage class"""
import json
import os
import time

from src.localStorage.consts import CLASSNAME
from src.localStorage.jsonEncoder.json_encoder import JsonEncoder
from src.shared.errors.file_empty_error import FileEmptyError
from src.shared.errors.file_not_readable_error import FileNotReadableError
from src.shared.errors.file_not_writable_error import FileNotWritableError


class LocalStorage:
    """Read/write json in file"""
    def __init__(self, filename: str):
        self.is_write = False
        self.data = None
        self.filename = filename
        self.path = os.path.dirname(__file__).split('src')[0]
        self.__create_file_if_not_exist()

    def __create_file_if_not_exist(self):
        try:
            with open(self.path + self.filename, 'x', encoding='utf-8'):
                pass
        except OSError:
            pass

    def _read(self):
        """Reading data in file"""
        while self.is_write:
            time.sleep(0.1)
        if self.data is not None:
            return json.loads(self.data)

        with open(self.path + self.filename, 'r', encoding='utf-8') as file:
            file.seek(0)
            if not file.readable():
                raise FileNotReadableError(CLASSNAME, self.filename)
            json_data = file.read()
            if json_data == '':
                raise FileEmptyError(CLASSNAME, self.filename)
            self.data = json_data
        return json.loads(self.data)

    def _write(self, data):
        """writing data in file"""
        self.is_write = True
        os.remove(self.path + self.filename)
        with open(self.path + self.filename, 'w', encoding='utf-8') as file:
            if not file.writable():
                raise FileNotWritableError(CLASSNAME, self.filename)
            file.write(json.dumps(data, indent=4, cls=JsonEncoder))
            self.data = json.dumps(data, indent=4, cls=JsonEncoder)
        self.is_write = False
