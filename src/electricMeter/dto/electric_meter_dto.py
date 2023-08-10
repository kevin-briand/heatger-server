"""object for config file"""
from dataclasses import dataclass


@dataclass
class ElectricMeterDto:
    """ElectricMeter data object"""

    # pylint: disable=unused-argument
    def __init__(self, enabled, gpio_input, **kwargs):
        self.enabled = enabled
        self.gpio_input = gpio_input
