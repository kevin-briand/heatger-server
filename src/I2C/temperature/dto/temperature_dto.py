"""object for config file"""

from dataclasses import dataclass


@dataclass
class TemperatureDto:
    """I2C temperature data object"""

    # pylint: disable=unused-argument
    def __init__(self, enabled, *args, **kwargs):
        self.enabled = enabled
