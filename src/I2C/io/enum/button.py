"""Button enum"""
from enum import Enum

from src.I2C.io.consts import PIN_BP_1, PIN_BP_2


class Button(Enum):
    """Button enum"""
    NEXT = PIN_BP_1
    OK = PIN_BP_2
