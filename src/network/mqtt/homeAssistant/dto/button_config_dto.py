"""ButtonConfigDto"""
import json
from dataclasses import dataclass

from src.network.mqtt.homeAssistant.consts import DEVICE_MANUFACTURER, DEVICE_NAME, BUTTON
from src.network.mqtt.generic_config_dto import GenericConfigDto


@dataclass
class ButtonConfigDto(GenericConfigDto):
    """mqtt data object for create a button in home assistant"""
    def __init__(self, name: str, payload=''):
        self.name = name
        self.data = payload

    def payload(self):
        """Return an object necessary to define a new button in home assistant"""
        response = {
            "name": self.name,
            "unique_id": self.name,
            "command_topic": BUTTON + F"{self.name}/commands",
            "payload_press": self.data,
            "os": 0,
            "retain": False,
            "entity_category": "config",
            "device": {
                "identifiers": ["heatger"],
                "manufacturer": DEVICE_MANUFACTURER,
                "name": DEVICE_NAME
            }
        }
        return response

    def to_object(self) -> dict:
        """return an object containing :\n
         - name: button name
         - url: url to publish config
         - payload: payload returned by payload function
         """
        return {
            'name': self.name,
            'url': F'{BUTTON}{self.name}/config',
            'payload': json.dumps(self.payload())
        }
