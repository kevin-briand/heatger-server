import json

from src.network.mqtt.homeAssistant.consts import SENSOR, DEVICE_MANUFACTURER, DEVICE_NAME


class PublishConfig:
    def __init__(self, name: str, device_class: str, unit_of_measurement=''):
        self.name = name
        self.device_class = device_class
        self.unit_of_measurement = unit_of_measurement

    @staticmethod
    def sensor_payload(name: str, device_class: str, unit_of_measurement=''):
        template = "{{ value_json." + name + "}}"
        return {
            "name": name,
            "unique_id": name,
            "unit_of_measurement": unit_of_measurement,
            "value_template": template,
            "device_class": device_class,
            "state_topic": SENSOR + "heatger/state",
            "device": {
                "identifiers": ["heatger"],
                "manufacturer": DEVICE_MANUFACTURER,
                "name": DEVICE_NAME
            }
        }

    def sensor(self) -> []:
        return {
            'name': self.name,
            'url': F'{SENSOR}{self.name}/config',
            'payload': json.dumps(PublishConfig.sensor_payload(self.name, self.device_class, self.unit_of_measurement))
        }
