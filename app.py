import time
from src.localStorage.config import Config
from src.network.network import Network
from src.zone.consts import ZONE
from src.zone.zone import Zone

if __name__ == '__main__':
    network = Network()

    i = 1
    config = Config().get_config()
    zones = []
    while config.get(F"{ZONE}{i}") is not None:
        zones.append(Zone(i, network))
        i = i+1

    while True:
        for zone in zones:
            zone.update_mqtt_data()
        time.sleep(5)

