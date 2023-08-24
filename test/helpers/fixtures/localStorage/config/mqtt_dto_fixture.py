from faker import Faker

from src.network.mqtt.dto.mqtt_dto import MqttDto


def mqtt_dto_fixture() -> MqttDto:
    fake = Faker()
    return MqttDto(True, '127.0.0.1', 1888, 'username', '')
