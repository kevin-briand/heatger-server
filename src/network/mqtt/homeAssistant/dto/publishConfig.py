import json

from src.network.mqtt.homeAssistant.consts import CLASS_TEMPERATURE, SENSOR, DEVICE_MANUFACTURER, DEVICE_NAME


def sensor_payload(name: str, unit_of_measurement=''):
    return {
        "name": name,
        "unique_id": "heatger_" + name,
        "unit_of_measurement": unit_of_measurement,
        "value_template": "{{ value_json." + name + " }}",
        "device_class": CLASS_TEMPERATURE,
        "state_topic": SENSOR + "heatger/state",
        "device": {
            "identifiers": ["heatger"],
            "manufacturer": DEVICE_MANUFACTURER,
            "name": DEVICE_NAME
        }
    }


class PublishConfig:
    def __init__(self, name: str, unit_of_measurement=''):
        self.name = name
        self.unit_of_measurement = unit_of_measurement

    def sensor(self) -> []:
        return {
            'name': self.name,
            'url': F'{SENSOR}{self.name}/config',
            'payload': json.dumps(sensor_payload(self.name, self.unit_of_measurement))
        }
