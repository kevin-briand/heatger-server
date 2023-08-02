"""LocalStorage class"""
import json
import os
import time
from typing import Optional

from src.localStorage.jsonEncoder.file_encoder import FileEncoder


class LocalStorage:
    """Read/write json in file"""
    _instance: Optional['LocalStorage'] = None
    _initialized = False
    _write = False

    def __new__(cls, *args, **kwargs) -> 'LocalStorage':
        if not isinstance(cls._instance, cls):
            cls._instance = super(LocalStorage, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, filename: str):
        if self._initialized:
            return

        self.data = None
        self.filename = filename
        self.path = os.path.dirname(__file__).split('src')[0]
        try:
            with open(self.path + filename, 'x', encoding='utf-8'):
                pass
        except OSError:
            pass

    def read(self):
        """Reading data in file"""
        while LocalStorage._write:
            time.sleep(0.1)
        if self.data is not None:
            return json.loads(self.data)

        with open(self.path + self.filename, 'r', encoding='utf-8') as file:
            file.seek(0)
            if not file.readable():
                raise FileNotFoundError
            json_data = file.read()
            if json_data != '':
                self.data = json_data
        return json.loads(self.data)

    def write(self, data):
        """writing data in file"""
        LocalStorage._write = True
        os.remove(self.path + self.filename)
        with open(self.path + self.filename, 'w', encoding='utf-8') as file:
            if file.writable():
                file.write(json.dumps(data, indent=4, cls=FileEncoder))
                self.data = json.dumps(data, indent=4, cls=FileEncoder)
        LocalStorage._write = False
