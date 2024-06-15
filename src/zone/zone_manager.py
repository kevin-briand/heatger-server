from typing import Optional

from src.shared.enum.state import State
from src.zone.zone import Zone


class ZoneManager:
    zones: [Zone] = []

    @staticmethod
    async def update_state(zone_id: str, state: State):
        from src.network.websocket.ws_server import WSServer
        await WSServer.update_state(zone_id, state)

    @staticmethod
    async def set_state(zone_id: str, state: State):
        try:
            zone: Optional[Zone] = None
            for z in ZoneManager.zones:
                if z.zone_id == zone:
                    zone = z
            if not zone:

                    zone = Zone(zone_id, ZoneManager.update_state)
                    ZoneManager.zones.append(zone)

            await zone.set_state(state)
        except Exception:
            pass
