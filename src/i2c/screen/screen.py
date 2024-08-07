"""Screen Class"""
import time
from typing import Optional

from luma.core.error import DeviceNotFoundError
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from smbus2 import SMBus

from src.i2c.screen.dto.zone_screen_dto import ZoneScreenDto
from src.i2c.screen.enum.vue import Vue
from src.i2c.screen.errors.write_error import WriteError
from src.i2c.screen.vues.general_vue import GeneralVue
from src.i2c.screen.vues.set_order_vue import SetOrderVue
from src.i2c.temperature.dto.sensor_dto import SensorDto
from src.localStorage.config.config import Config


class Screen:
    """Initialise and manage a I2C screen"""
    def __init__(self, bus: SMBus):
        device = Config().get_config().i2c.screen.device
        self.serial = i2c(bus=bus, address=device.address)
        self.device = sh1106(self.serial)
        self.current_vue = Vue.GENERAL
        self.zone_info: Optional[ZoneScreenDto] = None
        self.temperature_info: Optional[SensorDto] = None

    async def set_temperature(self, temperature_info: SensorDto) -> None:
        """set temperature_info"""
        self.temperature_info = temperature_info

    def set_zone_info(self, zone_info: ZoneScreenDto) -> None:
        """set zone_info"""
        self.zone_info = zone_info

    def show_next_vue(self) -> None:
        """show the next vue on the screen"""
        if self.current_vue.value < len(Vue) - 1:
            self.current_vue = Vue(self.current_vue.value + 1)
        else:
            self.current_vue = Vue.GENERAL
        self.draw_vue_if_vars_is_not_none()

    def get_current_vue(self) -> Vue:
        """return the current vue showed on the screen"""
        return self.current_vue

    def show_general_vue(self) -> None:
        """Show the general vue on the screen"""
        self.current_vue = Vue.GENERAL
        self.draw_vue_if_vars_is_not_none()

    def draw_vue_if_vars_is_not_none(self) -> None:
        """draw vue on the screen if temperature_info and zone_info is not None"""
        if not self.zone_info or not self.temperature_info:
            return
        retry = 0
        try:
            if self.current_vue == Vue.GENERAL:
                self.device.display(GeneralVue(self.zone_info, self.temperature_info).render())
            if self.current_vue == Vue.SET_STATE_ZONE1:
                self.device.display(SetOrderVue(self.zone_info.zone1_name, self.zone_info.zone1_state).render())
            if self.current_vue == Vue.SET_STATE_ZONE2:
                self.device.display(SetOrderVue(self.zone_info.zone2_name, self.zone_info.zone2_state).render())
            retry = 0
        except DeviceNotFoundError:
            retry += 1
            time.sleep(1)
            if retry == 3:
                raise WriteError()
            self.draw_vue_if_vars_is_not_none()

