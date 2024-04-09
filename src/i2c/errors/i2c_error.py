"""I2CError Exception"""
from typing import Optional

from src.localStorage.consts import CLASSNAME
from src.shared.logs.logs import Logs


class I2cError(Exception):
    """return a i2c exception"""

    def __init__(self, message: str, classname: Optional[str] = CLASSNAME):
        Logs.error(classname, message)
        super().__init__(F"{classname}: {message}")
