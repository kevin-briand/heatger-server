import datetime
import time
from src.localStorage.config import Config
from src.network.mqtt.consts import MQTT
from src.network.mqtt.homeAssistant.consts import PUBLISH_DATA_SENSOR
from src.network.network import Network
from src.shared.consts.consts import ENABLED
from src.shared.enum.orders import Orders
from src.shared.logs.logs import Logs
from src.zone.consts import ZONE
from src.zone.dto.horaire import Horaire
from src.zone.frostfree import Frostfree
from src.zone.zone import Zone

zones = []
frostfree: Frostfree = Frostfree(zones)
CLASSNAME = 'Heatger'


def on_mqtt_message(client, userdata, message):
    if message.retain:
        return
    if message.topic.__contains__(ZONE):
        number_zone = int(message.topic[len(message.topic) - 1]) - 1
        if message.topic.__contains__('ma_'):
            zones.__getitem__(number_zone).toggle_mode()
        elif message.topic.__contains__('state_'):
            zones.__getitem__(number_zone).toggle_order()
    elif message.topic.__contains__('frostfree'):
        data = message.payload.decode('utf-8')
        if data == '':
            Logs.error(CLASSNAME, F'{Orders.FROSTFREE} - empty data')
            return
        end_date = datetime.datetime.strptime(data, '%Y-%m-%dT%H:%M')
        if end_date is None:
            Logs.error(CLASSNAME, F'{Orders.FROSTFREE} - invalid date format')
            return
        global frostfree
        if end_date > datetime.datetime.now():
            frostfree.start(end_date)
        else:
            frostfree.stop()


if __name__ == '__main__':
    network = Network()

    zones.clear()
    i = 1
    config = Config().get_config()
    mqtt_enabled = config.get(MQTT).get(ENABLED)

    horaires = [
        Horaire(datetime.datetime.now().weekday(), datetime.time(datetime.datetime.now().hour, datetime.datetime.now().minute), Orders.ECO),
        Horaire(datetime.datetime.now().weekday(), datetime.time(datetime.datetime.now().hour, datetime.datetime.now().minute+1), Orders.COMFORT),
        Horaire(datetime.datetime.now().weekday(), datetime.time(datetime.datetime.now().hour, datetime.datetime.now().minute+2), Orders.ECO),
        Horaire(datetime.datetime.now().weekday(), datetime.time(datetime.datetime.now().hour, datetime.datetime.now().minute+3), Orders.COMFORT),
        Horaire(datetime.datetime.now().weekday(), datetime.time(datetime.datetime.now().hour, datetime.datetime.now().minute+4), Orders.ECO),
        Horaire(datetime.datetime.now().weekday(), datetime.time(datetime.datetime.now().hour, datetime.datetime.now().minute+5), Orders.COMFORT)
    ]
    Config().remove_all_horaire("zone1")
    Config().add_horaires('zone1', horaires)
    Config().remove_all_horaire("zone2")
    Config().add_horaires('zone2', horaires)

    while config.get(F"{ZONE}{i}") is not None:
        zones.append(Zone(i, network))
        if mqtt_enabled:
            while not network.mqtt.is_connected():
                continue
            network.mqtt.init_publish_zone(F"{ZONE}{i}")
            network.mqtt.init_subscribe_zone(F"{ZONE}{i}")
        i = i + 1
    if mqtt_enabled:
        network.mqtt.init_subscribe_global()
        network.mqtt.init_publish_global()
        network.mqtt.init_publish_i2c()
        network.mqtt.set_on_message(on_mqtt_message)

    frostfree.restore()

    while True:
        for zone in zones:
            network.mqtt.publish_data(PUBLISH_DATA_SENSOR, zone.get_data())
            network.mqtt.publish_data(PUBLISH_DATA_SENSOR, frostfree.get_data())
        time.sleep(5)




