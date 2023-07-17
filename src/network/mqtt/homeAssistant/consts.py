"""Const for homeassistant class"""
from src.network.ping.ping import Ping

DISCOVERY_PREFIX = 'homeassistant/'
DEVICE_IDENTIFIER = 'heatger'
DEVICE_MANUFACTURER = 'firedream'
DEVICE_NAME = 'heatger'
SENSOR = DISCOVERY_PREFIX + 'sensor/'
PUBLISH_DATA_SENSOR = SENSOR + DEVICE_NAME + '/state'
BUTTON = DISCOVERY_PREFIX + 'button/'
CLASS_TEMPERATURE = 'temperature'
CLASS_HUMIDITY = 'humidity'
CLASS_PRESSURE = 'pressure'
CLASS_DURATION = 'duration'
CLASS_ENERGY = 'energy'
CLASS_GENERIC = None
CLASS_DATE = 'timestamp'
CLASSNAME = 'HomeAssistant'
SECOND = 's'
BUTTON_AUTO = 'ma'
BUTTON_STATE = 'state'
BUTTON_FROSTFREE = 'frostfree'
FROSTFREE = 'frostfree'
TOTAL_INCREASING = 'total_increasing'
WH = 'Wh'
SWITCH_MODE = 'switch_mode'
SWITCH_STATE = 'switch_state'
PROG = 'prog'
DEVICE_INFO = {
    "identifiers": ["heatger"],
    "manufacturer": DEVICE_MANUFACTURER,
    "name": DEVICE_NAME,
    "connections": [
        ["ip", Ping.get_ip()]
    ]
}
