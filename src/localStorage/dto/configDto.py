from src.I2C.dto.i2cDto import I2CDto
from src.electricMeter.dto.electricMeterDto import ElectricMeterDto
from src.network.dto.networkDto import NetworkDto
from src.network.mqtt.dto.mqttDto import MqttDto
from src.zone.dto.zoneDto import ZoneDto


class InputDto(object):
    def __init__(self, electric_meter, *args, **kwargs):
        self.electric_meter = ElectricMeterDto(**electric_meter)


class ConfigDto(object):
    def __init__(self, mqtt, network, i2c, input, zone1, zone2, zone3=None, *args, **kwargs):
        self.mqtt = MqttDto(**mqtt)
        self.network = NetworkDto(**network)
        self.i2c = I2CDto(**i2c)
        self.input = InputDto(**input)
        self.zone1 = ZoneDto(**zone1)
        self.zone2 = ZoneDto(**zone2)
        if zone3 is not None:
            self.zone3 = ZoneDto(**zone3)
