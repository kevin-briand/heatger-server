import json

from src.network.mqtt.homeAssistant.consts import SENSOR, DEVICE_MANUFACTURER, DEVICE_NAME


class PublishConfig:
    def __init__(self, name: str, device_class: str, unit_of_measurement='', state_class=None):
        self.name = name
        self.device_class = device_class
        self.unit_of_measurement = unit_of_measurement
        self.state_class = state_class

    @staticmethod
    def sensor_payload(name: str, device_class: str, unit_of_measurement='', state_class=None):
        response = {
            "name": name,
            "unique_id": name,
            "value_template": "{{ value_json." + name + "}}",
            "device_class": device_class,
            "state_topic": SENSOR + "heatger/state",
            'unit_of_measurement': unit_of_measurement,
            "device": {
                "identifiers": ["heatger"],
                "manufacturer": DEVICE_MANUFACTURER,
                "name": DEVICE_NAME
            }
        }
        if state_class is not None:
            response['state_class'] = state_class

        return response

    def sensor(self) -> dict:
        return {
            'name': self.name,
            'url': F'{SENSOR}{self.name}/config',
            'payload': json.dumps(PublishConfig.sensor_payload(self.name, self.device_class, self.unit_of_measurement, self.state_class))
        }
