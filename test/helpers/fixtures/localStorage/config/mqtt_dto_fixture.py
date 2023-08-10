from faker import Faker

from src.network.mqtt.dto.mqtt_dto import MqttDto


def mqtt_dto_fixture() -> MqttDto:
    fake = Faker()
    return MqttDto(True, fake.ipv4(), fake.random.randint(5000, 8000), fake.name(), fake.name())
