"""object for config file"""
from dataclasses import dataclass

from src.i2c.dto.i2c_dto import I2CDto
from src.electricMeter.dto.electric_meter_dto import ElectricMeterDto
from src.network.api.dto.api_dto import ApiDto
from src.network.dto.network_dto import NetworkDto
from src.network.mqtt.dto.mqtt_dto import MqttDto
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
    def __init__(self, mqtt, network, i2c, entry, zone1, zone2, api, **kwargs):
        self.mqtt = mqtt if isinstance(mqtt, MqttDto) else MqttDto(**mqtt)
        self.network = network if isinstance(network, NetworkDto) else NetworkDto(**network)
        self.i2c = i2c if isinstance(i2c, I2CDto) else I2CDto(**i2c)
        self.entry = entry if isinstance(entry, InputDto) else InputDto(**entry)
        self.zone1 = zone1 if isinstance(zone1, ZoneDto) else ZoneDto(**zone1)
        self.zone2 = zone2 if isinstance(zone2, ZoneDto) else ZoneDto(**zone2)
        self.api = api if isinstance(api, ApiDto) else ApiDto(**api)
