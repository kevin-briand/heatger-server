"""Heatger main app"""
from src.electricMeter.electric_meter import ElectricMeter
from src.i2c.i2c import I2C
from src.network.websocket.ws_server import WSServer
from src.zone.zone_manager import ZoneManager

ws_server = WSServer()


def main():
    em = ElectricMeter()
    i2c = I2C()
    ZoneManager.init()
    i2c.toggle_order = ZoneManager.toggle_order
    ws_server.start()


if __name__ == '__main__':
    main()
