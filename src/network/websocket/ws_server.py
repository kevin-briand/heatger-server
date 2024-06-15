import asyncio
import json

import socket

import aiohttp
from aiohttp import web, WSMessage
from aiohttp.web_ws import WebSocketResponse

from src.localStorage.config.config import Config
from src.localStorage.json_encoder.json_encoder import JsonEncoder
from src.shared.enum.state import State


class WSServer:
    """Websocket Server"""
    Clients: [WebSocketResponse] = []

    def __init__(self):
        self.app = aiohttp.web.Application()
        self.app.router.add_route('GET', '/ws', self.websocket_handler)
        print('WS Started')

    @staticmethod
    async def websocket_handler(request):
        ws = aiohttp.web.WebSocketResponse()
        await ws.prepare(request)
        WSServer.Clients.append(ws)
        print('Websocket connection ready')

        try:
            while True:
                data: WSMessage = await asyncio.shield(ws.receive())
                if data.type == aiohttp.WSMsgType.TEXT:
                    print(data.data)
                    if data.data == 'close':
                        await ws.close()
                        break
                    else:
                        await WSServer.eval_message(data.data)
                elif data.type in (aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.ERROR):
                    await ws.close()
                    WSServer.Clients.remove(ws)
                    break
        except asyncio.CancelledError:
            pass
        print('Client disconnected')
        return ws

    @staticmethod
    async def eval_message(data: any):
        from src.zone.zone_manager import ZoneManager
        data = json.loads(data)
        if 'state' in data:
            for key, value in data.get('state').items():
                print(F'receipt new state: {key} -> {State(value)}')

                await ZoneManager.set_state(key, State(value))

    def start(self):
        aiohttp.web.run_app(self.app, host='0.0.0.0', port=Config().get_port())

    @staticmethod
    async def update_state(zone: str, state: State):
        for ws in WSServer.Clients:
            await ws.send_json({'state': {zone: state}}, dumps=lambda obj: json.dumps(obj, cls=JsonEncoder))

    @staticmethod
    async def update_electric_meter(value: int):
        for ws in WSServer.Clients:
            await ws.send_json({'electric_meter': value})

    @staticmethod
    async def listen_udp():
        loop = asyncio.get_event_loop()
        udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        udp_sock.bind(('', 5001))
        udp_sock.setblocking(False)  # Set socket to non-blocking mode
        print("Écoute UDP sur le port 5001")

        while True:
            data, addr = await loop.sock_recv(udp_sock, 1024)  # Use asyncio loop to receive data
            print(f"Message UDP reçu de {addr}: {data.decode()}")
            if data.decode() == 'Heatger':
                response = 'OK'
                await loop.sock_sendall(udp_sock, response.encode())  # Use asyncio loop to send data
                break
        udp_sock.close()
