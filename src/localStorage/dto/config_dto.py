"""object for config file"""
from dataclasses import dataclass

from src.I2C.dto.i2c_dto import I2CDto
from src.electricMeter.dto.electric_meter_dto import ElectricMeterDto
from src.network.api.dto.api_dto import ApiDto
from src.network.dto.network_dto import NetworkDto
from src.network.mqtt.dto.mqtt_dto import MqttDto
from src.zone.dto.zone_dto import ZoneDto


@dataclass
class InputDto:
    """Input data object"""

    # pylint: disable=unused-argument
    def __init__(self, electric_meter, *args, **kwargs):
        self.electric_meter = ElectricMeterDto(**electric_meter)


@dataclass
class ConfigDto:
    """Config data object"""

    # pylint: disable=unused-argument
    def __init__(self, mqtt, network, i2c, entry, zone1, zone2, api, *args, **kwargs):
        self.mqtt = MqttDto(**mqtt)
        self.network = NetworkDto(**network)
        self.i2c = I2CDto(**i2c)
        self.entry = InputDto(**entry)
        self.zone1 = ZoneDto(**zone1)
        self.zone2 = ZoneDto(**zone2)
        self.api = ApiDto(**api)
