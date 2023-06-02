"""object for config file"""
from dataclasses import dataclass


@dataclass
class IODto:
    """I2C io data object"""

    # pylint: disable=unused-argument
    def __init__(self, enabled, *args, **kwargs):
        self.enabled = enabled
