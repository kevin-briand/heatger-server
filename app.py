"""Heatger main app"""
import datetime
import platform

from src.network.api.api import Api
from src.electricMeter.electric_meter import ElectricMeter
from src.localStorage.config import Config
from src.network.network import Network
from src.shared.enum.orders import Orders
from src.zone.dto.horaire_dto import HoraireDto
from src.zone.zone_manager import ZoneManager

if __name__ == '__main__':
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

    network = Network()
    zone_manager = ZoneManager(network)
    zone_manager.start()

    em = ElectricMeter()

    api = None
    if platform.system().lower() != 'windows':
        api = Api().start()
    else:
        api = Api().start_debug()

