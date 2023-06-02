"""LocalStorage class"""
import json
import os
from src.localStorage.jsonEncoder.file_encoder import FileEncoder


class LocalStorage:
    """Read/write json in file"""
    def __init__(self, filename: str):
        self.filename = filename
        try:
            with open(filename, 'x', encoding='utf-8'):
                pass
        except OSError:
            pass

    def read(self):
        """Reading data in file"""
        with open(self.filename, 'r', encoding='utf-8') as file:
            file.seek(0)
            if file.readable():
                json_data = file.read()
                if json_data == '':
                    return {}
                return json.loads(json_data)
        return {}

    def write(self, data):
        """writing data in file"""
        os.remove(self.filename)
        with open(self.filename, 'w', encoding='utf-8') as file:
            if file.writable():
                file.write(json.dumps(data, indent=4, cls=FileEncoder))
