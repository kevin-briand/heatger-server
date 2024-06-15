"""Zone class"""
from typing import Coroutine, Callable

from src.localStorage.config.config import Config
from src.pilot.pilot import Pilot
from src.shared.enum.state import State
from src.shared.logs.logs import Logs


class Zone:
    """This class define a new heaters zone"""

    def __init__(self, zone_id: str, upd_state_callback: Callable[[str, State], Coroutine[None, None, None]]):
        super().__init__()
        config = Config().get_zone(zone_id)
        if config is None:
            raise Exception(F'{zone_id} is not defined in config.json')
        self.zone_id = zone_id
        self.name = config.name
        self.current_state = State.ECO
        self.pilot = Pilot(config.gpio_eco, config.gpio_frostfree, True)
        self.upd_state = upd_state_callback

    async def set_state(self, state: State) -> None:
        """change state"""
        Logs.info(self.zone_id, F'zone {self.name} switch {self.current_state.name} to {state.name}')
        self.current_state = state
        self.pilot.set_state(state)
        await self.upd_state(self.zone_id, state)
