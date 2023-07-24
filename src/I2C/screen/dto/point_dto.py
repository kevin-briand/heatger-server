"""Point object"""
from dataclasses import dataclass


@dataclass
class PointDto:
    """point object"""

    # pylint: disable=C0103
    def __init__(self, x: int, y: int):
        self.x = x  # pylint: disable=C0103
        self.y = y  # pylint: disable=C0103
