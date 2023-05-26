import json
from threading import Thread

from websockets.sync.client import connect


class WebSocket(Thread):
    def __init__(self, host: str, port: int):
        super().__init__()
        print('Init WebSocket...')
        self.client = None
        self.host = host
        self.port = port
        self.connected = False

    def run(self) -> None:
        while True:
            if not self.connected:
                self.connect()
            message = json.loads(self.client.recv())
            if message:
                if message['type'] == 'auth_required':
                    auth = json.dumps({"type": "auth",
                                       "access_token": ""})
                    print(auth)
                    self.client.send(auth)
                    print('token send')
                elif message['type'] == 'auth_ok':
                    print('Authentified')
                    self.client.send(json.dumps({
                        "id": 1,
                        "type": "get_states",
                    }))
                else:
                    print(message)
                message = None

    def connect(self):
        print('WebSocket - Connect to ' + self.host + ':' + str(self.port))
        self.client = connect(F"ws://{self.host}:{self.port}/api/websocket?latest")
        self.connected = True
        # websocket.send("Hello world!")
        # message = self.client.recv()
        # print(f"Received: {message}")
