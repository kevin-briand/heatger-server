from enum import Enum


class Mode(Enum):
    AUTO = 0
    MANUAL = 1

    @staticmethod
    def to_mode(mode_num: int):
        if mode_num == Mode.AUTO.value:
            return Mode.AUTO
        else:
            return Mode.MANUAL
