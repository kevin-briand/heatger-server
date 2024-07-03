"""Websocket server"""
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

    @staticmethod
    async def websocket_handler(request):
        """WS loop, called when client connects to the server"""
        ws = aiohttp.web.WebSocketResponse()
        await ws.prepare(request)
        WSServer.Clients.append(ws)

        try:
            while True:
                data: WSMessage = await asyncio.shield(ws.receive())
                if data.type == aiohttp.WSMsgType.TEXT:
                    if data.data == 'close':
                        await ws.close()
                        break
                    else:
                        await WSServer.eval_message(data.data, ws)
                elif data.type in (aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.ERROR):
                    await ws.close()
                    WSServer.Clients.remove(ws)
                    break
        except asyncio.CancelledError:
            pass
        return ws

    @staticmethod
    async def eval_message(data: any, client: WebSocketResponse):
        """Evaluate the message received by the client"""
        from src.zone.zone_manager import ZoneManager
        data = json.loads(data)
        if 'state' in data:
            for key, value in data.get('state').items():
                await ZoneManager.set_state(key, State(value))
        if 'config' in data:
            await client.send_json({'config': Config().get_config()}, dumps=lambda obj: json.dumps(obj, cls=JsonEncoder))

    def start(self):
        """Start the server"""
        aiohttp.web.run_app(self.app, host='0.0.0.0', port=Config().get_port())

    @staticmethod
    async def update_state(zone: str, state: State):
        """Send the new zone state to the client"""
        for ws in WSServer.Clients:
            await ws.send_json({'state': {zone: state}}, dumps=lambda obj: json.dumps(obj, cls=JsonEncoder))

    @staticmethod
    async def update_electric_meter(value: int):
        """Send the electricity meter reading to the client"""
        for ws in WSServer.Clients:
            await ws.send_json({'electric_meter': value})

    @staticmethod
    async def update_temperature(data: {}):
        """Send the current temperature to the client"""
        for ws in WSServer.Clients:
            await ws.send_json({'temperature': data})

    @staticmethod
    async def listen_udp():
        """Unused"""
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
