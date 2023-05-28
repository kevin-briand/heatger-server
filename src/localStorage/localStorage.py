import json
import os


class LocalStorage:
    def __init__(self, filename: str):
        self.filename = filename
        try:
            open(filename, 'x')
        except OSError:
            pass

    def read(self) -> dict:
        file = open(self.filename, 'r')
        file.seek(0)
        if file.readable():
            json_data = file.read()
            if json_data == '':
                return {}
            return json.loads(json_data)
        file.close()

    def write(self, data):
        os.remove(self.filename)
        file = open(self.filename, 'w')
        if file.writable():
            file.write(json.dumps(data))
        file.close()
