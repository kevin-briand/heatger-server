"""object for config file"""
from dataclasses import dataclass

from src.i2c.dto.i2c_dto import I2CDto
from src.electricMeter.dto.electric_meter_dto import ElectricMeterDto
from src.zone.dto.zone_dto import ZoneDto


@dataclass
class InputDto:
    """Input data object"""

    # pylint: disable=unused-argument
    def __init__(self, electric_meter, **kwargs):
        self.electric_meter = electric_meter if isinstance(electric_meter, ElectricMeterDto) \
            else ElectricMeterDto(**electric_meter)


@dataclass
class ConfigDto:
    """Config data object"""

    # pylint: disable=unused-argument
    def __init__(self, i2c, entry, zone1, zone2, ws_port=None, **kwargs):
        self.i2c = i2c if isinstance(i2c, I2CDto) else I2CDto(**i2c)
        self.entry = entry if isinstance(entry, InputDto) else InputDto(**entry)
        self.zone1 = zone1 if isinstance(zone1, ZoneDto) else ZoneDto(**zone1)
        self.zone2 = zone2 if isinstance(zone2, ZoneDto) else ZoneDto(**zone2)
        self.ws_port = ws_port if ws_port else None
