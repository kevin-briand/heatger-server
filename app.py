"""Heatger main app"""
import datetime
import time

from src.electricMeter.electric_meter import ElectricMeter
from src.localStorage.config import Config
from src.network.mqtt.homeAssistant.consts import PUBLISH_DATA_SENSOR, \
    BUTTON_AUTO, BUTTON_FROSTFREE, BUTTON_STATE
from src.network.network import Network
from src.shared.enum.orders import Orders
from src.shared.logs.logs import Logs
from src.zone.consts import ZONE
from src.zone.dto.horaire_dto import HoraireDto
from src.zone.frostfree import Frostfree
from src.zone.zone import Zone

zones = []
frostfree: Frostfree = Frostfree(zones)
CLASSNAME = 'Heatger'


# pylint: disable=unused-argument
def on_mqtt_message(client, userdata, message):
    """processing of messages received by mqtt"""
    if message.retain:
        return
    if ZONE in message.topic:
        number_zone = int(message.topic[len(message.topic) - 1]) - 1
        if F'{BUTTON_AUTO}_' in message.topic:
            zones[number_zone].toggle_mode()
        elif F'{BUTTON_STATE}_' in message.topic:
            zones[number_zone].toggle_order()
    elif BUTTON_FROSTFREE in message.topic:
        data = message.payload.decode('utf-8')
        if data == '':
            Logs.error(CLASSNAME, F'{Orders.FROSTFREE} - empty data')
            return
        end_date = datetime.datetime.strptime(data, '%Y-%m-%dT%H:%M')
        if end_date is None:
            Logs.error(CLASSNAME, F'{Orders.FROSTFREE} - invalid date format')
            return
        if end_date > datetime.datetime.now():
            frostfree.start(end_date)
        else:
            frostfree.stop()


if __name__ == '__main__':
    network = Network()

    zones.clear()
    i = 1
    config = Config().get_config()
    mqtt_enabled = config.mqtt.enabled

    # TEST -----------------------------------------
    horaires = [
        HoraireDto(datetime.datetime.now().weekday(),
                   datetime.time(datetime.datetime.now().hour, datetime.datetime.now().minute),
                   Orders.ECO),
        HoraireDto(datetime.datetime.now().weekday(),
                   datetime.time(datetime.datetime.now().hour, datetime.datetime.now().minute + 1),
                   Orders.COMFORT),
        HoraireDto(datetime.datetime.now().weekday(),
                   datetime.time(datetime.datetime.now().hour, datetime.datetime.now().minute + 2),
                   Orders.ECO),
        HoraireDto(datetime.datetime.now().weekday(),
                   datetime.time(datetime.datetime.now().hour, datetime.datetime.now().minute + 3),
                   Orders.COMFORT),
        HoraireDto(datetime.datetime.now().weekday(),
                   datetime.time(datetime.datetime.now().hour, datetime.datetime.now().minute + 4),
                   Orders.ECO),
        HoraireDto(datetime.datetime.now().weekday(),
                   datetime.time(datetime.datetime.now().hour, datetime.datetime.now().minute + 5),
                   Orders.COMFORT)
    ]
    Config().remove_all_horaire("zone1")
    Config().add_horaires('zone1', horaires)
    Config().remove_all_horaire("zone2")
    Config().add_horaires('zone2', horaires)
    Config().add_ip('192.168.1.5')
    # ---------------------------------------------

    try:
        while getattr(config, F"{ZONE}{i}") is not None:
            zones.append(Zone(i, network))
            if mqtt_enabled:
                while not network.mqtt.is_connected():
                    continue
                network.mqtt.init_publish_zone(F"{ZONE}{i}")
                network.mqtt.init_subscribe_zone(F"{ZONE}{i}")
            i = i + 1
    except AttributeError:
        pass

    if mqtt_enabled:
        network.mqtt.init_subscribe_global()
        network.mqtt.init_publish_global()
        network.mqtt.init_publish_i2c()
        network.mqtt.set_on_message(on_mqtt_message)

    em = ElectricMeter()

    frostfree.restore()

    while True:
        for zone in zones:
            network.mqtt.publish_data(PUBLISH_DATA_SENSOR, zone.get_data())
        network.mqtt.publish_data(PUBLISH_DATA_SENSOR, frostfree.get_data())
        network.mqtt.publish_data(PUBLISH_DATA_SENSOR, em.get_data())
        time.sleep(5)
