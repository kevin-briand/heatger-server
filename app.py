"""Heatger main app"""
from src.network.websocket.ws_server import WSServer

ws_server = WSServer()


def main():
    ws_server.start()


if __name__ == '__main__':
    main()
