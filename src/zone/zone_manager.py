import asyncio
from typing import Optional

from src.i2c.i2c import I2C
from src.i2c.screen.dto.zone_screen_dto import ZoneScreenDto
from src.localStorage.config.config import Config
from src.shared.enum.state import State
from src.zone.consts import ZONE
from src.zone.zone import Zone


class ZoneManager:
    zones: [Zone] = []
    loop = None

    @staticmethod
    def init():
        """Initialize the class"""
        if not asyncio.get_event_loop():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        ZoneManager.loop = asyncio.get_event_loop()
        # init zones
        i = 1
        zones = Config().get_config().zones
        try:
            while zones[F"{ZONE}{i}"] is not None:
                zone = Zone(F"{ZONE}{i}", ZoneManager.update_state)
                ZoneManager.zones.append(zone)
                i += 1
        except KeyError:
            pass

    @staticmethod
    async def update_state(zone_id: str, state: State):
        """Send Updating the zone state"""
        from src.network.websocket.ws_server import WSServer
        await WSServer.update_state(zone_id, state)
        await ZoneManager.update_i2c_data()

    @staticmethod
    async def set_state(zone_id: str, state: State):
        """Update zone state"""
        zone: Optional[Zone] = None
        for z in ZoneManager.zones:
            if z.zone_id == zone_id:
                zone = z
        await zone.set_state(state)

    @staticmethod
    async def toggle_order(zone_id: str):
        """Switch zone order between comfort and eco"""
        for z in ZoneManager.zones:
            if z.zone_id == zone_id:
                await z.set_state(State.ECO if z.current_state == State.COMFORT else State.COMFORT)

    @staticmethod
    async def update_i2c_data():
        """Send data to i2c"""
        zone_data = ZoneScreenDto()
        for zone in ZoneManager.zones:
            if zone.zone_id == F"{ZONE}1":
                zone_data.zone1_name = zone.zone_id
                zone_data.zone1_state = zone.current_state
            elif zone.zone_id == F"{ZONE}2":
                zone_data.zone2_name = zone.zone_id
                zone_data.zone2_state = zone.current_state
        await I2C().set_zones_datas_and_update_screen(zone_data)
