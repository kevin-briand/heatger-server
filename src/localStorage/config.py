from src.localStorage.localStorage import LocalStorage


class Config(LocalStorage):
    def __init__(self):
        super().__init__('config.json')
        self.config = self.read()

    def get_config(self):
        return self.config

    def set_config(self, key: str, value: str):
        self.config[key] = value
        self.write(self.config)
