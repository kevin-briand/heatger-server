"""object for config file"""
from dataclasses import dataclass


@dataclass
class ZoneDto:
    """zone data object"""

    # pylint: disable=unused-argument
    def __init__(self, name: str, gpio_eco: int, gpio_frostfree: int, **kwargs):
        self.name = name
        self.gpio_eco = gpio_eco
        self.gpio_frostfree = gpio_frostfree
