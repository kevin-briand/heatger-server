"""object for config file"""
from dataclasses import dataclass

from src.i2c.dto.device_dto import DeviceDto


@dataclass
class ScreenDto:
    """I2C screen data object"""

    # pylint: disable=unused-argument
    def __init__(self, enabled, device, **kwargs):
        self.enabled = enabled
        self.device = device if isinstance(device, DeviceDto) else DeviceDto(**device)
