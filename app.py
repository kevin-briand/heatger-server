import time
from src.localStorage.config import Config
from src.network.mqtt.consts import MQTT
from src.network.mqtt.homeAssistant.consts import PUBLISH_DATA_SENSOR
from src.network.network import Network
from src.shared.consts.consts import ENABLED
from src.zone.consts import ZONE
from src.zone.zone import Zone

zones = []

def on_mqtt_message(client, userdata, message):
    number_zone = int(message.topic[len(message.topic)-1])-1
    if message.topic.__contains__('ma_'):
        zones.__getitem__(number_zone).toggle_mode()
    elif message.topic.__contains__('state_'):
        zones.__getitem__(number_zone).toggle_order()


if __name__ == '__main__':
    network = Network()

    zones.clear()
    i = 1
    config = Config().get_config()
    mqtt_enabled = config.get(MQTT).get(ENABLED)

    while config.get(F"{ZONE}{i}") is not None:
        zones.append(Zone(i, network))
        if mqtt_enabled:
            while not network.mqtt.is_connected():
                continue
            network.mqtt.init_publish_zone(F"{ZONE}{i}")
            network.mqtt.init_subscribe_zone(F"{ZONE}{i}")
        i = i + 1
    if mqtt_enabled:
        network.mqtt.init_publish_i2c()
        network.mqtt.set_on_message(on_mqtt_message)

    while True:
        for zone in zones:
            network.mqtt.publish_data(PUBLISH_DATA_SENSOR, zone.get_data())
        time.sleep(5)
