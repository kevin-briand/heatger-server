import json
import os


class LocalStorage:
    def __init__(self, filename: str):
        self.filename = filename

    def read(self):
        file = open(self.filename, 'r')
        file.seek(0)
        if file.readable():
            return json.loads(file.read())
        file.close()

    def write(self, data):
        os.remove(self.filename)
        file = open(self.filename, 'w')
        if file.writable():
            file.write(json.dumps(data))
        file.close()
