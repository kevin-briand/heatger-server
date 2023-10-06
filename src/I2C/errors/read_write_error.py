"""ReadWriteError Exception"""
from src.i2c.errors.i2c_error import I2cError
from src.i2c.screen.consts import CLASSNAME


class ReadWriteError(I2cError):
    """return a read/write exception"""

    def __init__(self):
        super().__init__("Failure to read/write to the bus", CLASSNAME)
