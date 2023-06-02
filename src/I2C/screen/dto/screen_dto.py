"""object for config file"""
from dataclasses import dataclass


@dataclass
class ScreenDto:
    """I2C screen data object"""

    # pylint: disable=unused-argument
    def __init__(self, enabled, *args, **kwargs):
        self.enabled = enabled
