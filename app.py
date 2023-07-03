"""Heatger main app"""
import datetime
import json
import platform
import time
from threading import Thread

from src.network.api.api import Api
from src.electricMeter.electric_meter import ElectricMeter
from src.localStorage.config import Config
from src.localStorage.jsonEncoder.file_encoder import FileEncoder
from src.network.mqtt.homeAssistant.consts import PUBLISH_DATA_SENSOR, \
    BUTTON_FROSTFREE, SWITCH_MODE, SWITCH_STATE
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
        number_zone = Zone.get_zone_number(message.topic)
        if number_zone == -1:
            return
        if F'_{SWITCH_MODE}' in message.topic:
            zones[number_zone].toggle_mode()
        elif F'_{SWITCH_STATE}' in message.topic:
            zones[number_zone].toggle_order()
    elif BUTTON_FROSTFREE in message.topic:
        payload = message.payload.decode('utf-8')
        if payload == '':
            Logs.error(CLASSNAME, F'{Orders.FROSTFREE} - empty data')
            return
        end_date = datetime.datetime.strptime(payload, '%Y-%m-%dT%H:%M')
        if end_date is None:
            Logs.error(CLASSNAME, F'{Orders.FROSTFREE} - invalid date format')
            return
        if end_date > datetime.datetime.now():
            frostfree.start(end_date)
        else:
            frostfree.stop()


old_data = {}


def refresh_mqtt_datas():
    global old_data
    while True:
        data = {}
        for zone in zones:
            data.update(zone.get_data().to_object())
        data.update(frostfree.get_data().to_object())
        if data != old_data:
            network.mqtt.publish_data(PUBLISH_DATA_SENSOR, json.dumps(data, cls=FileEncoder))
            old_data = data
        # network.mqtt.publish_data(PUBLISH_DATA_SENSOR, em.get_data())
        time.sleep(0.5)


if __name__ == '__main__':
    network = Network()

    zones.clear()
    i = 1
    config = Config().get_config()
    mqtt_enabled = config.mqtt.enabled

    # TEST -----------------------------------------
    minute = datetime.datetime.now().minute
    horaires = [
        HoraireDto(datetime.datetime.now().weekday(),
                   datetime.time(datetime.datetime.now().hour, minute),
                   Orders.ECO),
        HoraireDto(datetime.datetime.now().weekday(),
                   datetime.time(datetime.datetime.now().hour, minute + 1 if minute + 1 <= 59 else minute + 1 - 60),
                   Orders.COMFORT),
        HoraireDto(datetime.datetime.now().weekday(),
                   datetime.time(datetime.datetime.now().hour, minute + 2 if minute + 2 <= 59 else minute + 2 - 60),
                   Orders.ECO),
        HoraireDto(datetime.datetime.now().weekday(),
                   datetime.time(datetime.datetime.now().hour, minute + 3 if minute + 3 <= 59 else minute + 3 - 60),
                   Orders.COMFORT),
        HoraireDto(datetime.datetime.now().weekday(),
                   datetime.time(datetime.datetime.now().hour, minute + 4 if minute + 4 <= 59 else minute + 4 - 60),
                   Orders.ECO),
        HoraireDto(datetime.datetime.now().weekday(),
                   datetime.time(datetime.datetime.now().hour, minute + 5 if minute + 5 <= 59 else minute + 5 - 60),
                   Orders.COMFORT)
    ]
    Config().remove_all_horaire("zone1")
    Config().add_horaires('zone1', horaires)
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

    refresh_mqtt_datas = Thread(target=refresh_mqtt_datas)
    refresh_mqtt_datas.start()

    api = None
    if platform.system().lower() != 'windows':
        api = Api().start()
    else:
        api = Api().start_debug()

