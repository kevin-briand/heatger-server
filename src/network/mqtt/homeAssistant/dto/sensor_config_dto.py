"""PublishConfigDto"""
import json
from dataclasses import dataclass

from src.network.mqtt.generic_config_dto import GenericConfigDto
from src.network.mqtt.homeAssistant.consts import SENSOR, DEVICE_INFO


@dataclass
class SensorConfigDto(GenericConfigDto):
    """mqtt data object for create a sensor in home assistant"""
    def __init__(self, name: str, device_class: str, unit_of_measurement='', state_class=None):
        self.name = name
        self.device_class = device_class
        self.unit_of_measurement = unit_of_measurement
        self.state_class = state_class

    def payload(self):
        """Return an object necessary to define a new sensor in home assistant"""
        response = {
            "name": self.name,
            "unique_id": self.name,
            "value_template": "{{ value_json." + self.name + "}}",
            "state_topic": SENSOR + "heatger/state",
            "device": DEVICE_INFO
        }
        if self.device_class is not None:
            response['device_class'] = self.device_class
        if self.unit_of_measurement != '':
            response['unit_of_measurement'] = self.unit_of_measurement
        if self.state_class is not None:
            response['state_class'] = self.state_class

        return response

    def to_object(self) -> dict:
        """return an object containing :\n
         - name: sensor name
         - url: url to publish config
         - payload: payload returned by payload function
         """
        return {
            'name': self.name,
            'url': F'{SENSOR}{self.name}/config',
            'payload': json.dumps(self.payload())
        }
