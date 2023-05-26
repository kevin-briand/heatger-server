import time
from datetime import datetime

from flask import Flask, json

from src.network.mqtt.homeAssistant.homeAssistant import HomeAssistant
from src.network.network import Network
from src.network.websocket.websocket import WebSocket
from src.shared.enum.orders import Orders
from src.zone.dto.horaire import Horaire
from src.zone.zone import Zone

# app = Flask(__name__)


# @app.route('/')
# def hello_world():  # put application's code here
#     return json.jsonify(test="test", test2=0)


if __name__ == '__main__':
    network = Network(['192.168.1.157'], True)

    cv = Zone(1, network)

    hass_mqtt = HomeAssistant()
    hass_mqtt.start()

    #ws = WebSocket('192.168.1.5', 8123)
    #ws.start()

    while True:
        #print(cv.get_remaining_time())
        time.sleep(1)
