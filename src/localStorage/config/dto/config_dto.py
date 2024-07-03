"""object for config file"""
from dataclasses import dataclass
from typing import Dict

from src.i2c.dto.i2c_dto import I2CDto
from src.electricMeter.dto.electric_meter_dto import ElectricMeterDto
from src.zone.dto.zone_dto import ZoneDto


@dataclass
class InputDto:
    """Input data object"""
    def __init__(self, electric_meter, **kwargs):
        self.electric_meter = electric_meter if isinstance(electric_meter, ElectricMeterDto) \
            else ElectricMeterDto(**electric_meter)


@dataclass
class ConfigDto:
    """Config data object"""
    def __init__(self, i2c, entry, zones, ws_port=None, **kwargs):
        self.i2c = i2c if isinstance(i2c, I2CDto) else I2CDto(**i2c)
        self.entry = entry if isinstance(entry, InputDto) else InputDto(**entry)
        self.zones: Dict[str, ZoneDto] = {}
        for i, (key, zone) in enumerate(zones.items()):
            self.zones[F'zone{i + 1}'] = zone if isinstance(zone, ZoneDto) else ZoneDto(**zone)
        self.ws_port = ws_port if ws_port else None
