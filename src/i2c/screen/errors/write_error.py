"""WriteError Exception"""
from src.i2c.errors.i2c_error import I2cError
from src.i2c.screen.consts import CLASSNAME


class WriteError(I2cError):
    """return a write screen exception"""

    def __init__(self):
        super().__init__("Failure to write data to the screen", CLASSNAME)
