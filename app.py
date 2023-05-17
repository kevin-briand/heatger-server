import time
from datetime import datetime

from flask import Flask, json

from src.network.network import Network
from src.shared.enum.orders import Orders
from src.zone.dto.horaire import Horaire
from src.zone.zone import Zone

# app = Flask(__name__)


# @app.route('/')
# def hello_world():  # put application's code here
#     return json.jsonify(test="test", test2=0)


if __name__ == '__main__':
    network = Network(['192.168.1.157'], True)
    now = datetime.now()
    horaires = [Horaire(1, datetime(now.year, now.month, 1, 8,49), Orders.COMFORT),
                Horaire(5, datetime(now.year, now.month, 1, 8, 50), Orders.COMFORT)]
    cv = Zone('1', network, horaires, True)
    while True:
        print(cv.get_remaining_time())
        time.sleep(1)
