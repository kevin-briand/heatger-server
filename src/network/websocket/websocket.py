import asyncio
from websockets.sync.client import connect

class WebSocket:
    def __init__(self, host):
        self.host = host

    def connect(self):
        with connect("ws://localhost:8765") as websocket:
            websocket.send("Hello world!")
        message = websocket.recv()
        print(f"Received: {message}")