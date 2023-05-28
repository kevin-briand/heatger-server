import abc

from src.I2C.consts import CLASSNAME
from src.shared.logs.logs import Logs


class Temperature(metaclass=abc.ABCMeta):
    def __init__(self, gpio: int):
        self.pin = gpio
        Logs.info(CLASSNAME, 'Init temperature...')

    @abc.abstractmethod
    def get_values(self) -> []:
        raise NotImplementedError
