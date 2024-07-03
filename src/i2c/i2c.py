"""I2C manager"""
import asyncio
import threading
from typing import Optional, Callable, Coroutine

from smbus2 import SMBus

from src.i2c.errors.read_write_error import ReadWriteError
from src.i2c.io.enum.button import Button
from src.i2c.io.pcf8574.pcf8574 import Pcf8574
from src.i2c.screen.dto.zone_screen_dto import ZoneScreenDto
from src.i2c.screen.enum.device import Device
from src.i2c.screen.enum.vue import Vue
from src.i2c.screen.screen import Screen
from src.i2c.temperature.bme280.bme_280 import BME280
from src.i2c.temperature.dto.sensor_dto import SensorDto
from src.localStorage.config.config import Config
from src.i2c.consts import CLASSNAME, ZONE1, ZONE2
from src.network.websocket.ws_server import WSServer
from src.shared.logs.logs import Logs
from src.zone.consts import ZONE


class I2C:
    """I2C Manager class, run a event loop for update I2C devices"""
    _instance: Optional['I2C'] = None
    _initialized = False

    def __new__(cls, *args, **kwargs) -> 'I2C':
        if not isinstance(cls._instance, cls):
            cls._instance = super(I2C, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self.bus = SMBus(1)
        self.run_loop = True
        self.temperature_sensor: Optional[BME280] = None
        self.io_device: Optional[Pcf8574] = None
        self.screen_device: Optional[Screen] = None
        if self.is_device_enabled(Device.TEMPERATURE):
            self.temperature_sensor = BME280(self.bus)
        if self.is_device_enabled(Device.IO):
            self.io_device = Pcf8574()
        if self.is_device_enabled(Device.SCREEN):
            self.screen_device = Screen(self.bus)
        self.temperature: Optional[SensorDto] = None
        self.zones_datas: Optional[ZoneScreenDto] = None
        self.screen_need_update = False
        self.toggle_order: Optional[Callable[[str], Coroutine[None, None, int]]] = None
        self.loop_iterations = 0
        self.loop = asyncio.new_event_loop()
        self.start_main_loop()
        self._initialized = True

    @staticmethod
    def is_device_enabled(device: Device) -> bool:
        i2c = Config().get_config().i2c
        if device == Device.TEMPERATURE:
            return i2c.temperature.enabled
        elif device == Device.SCREEN:
            return i2c.screen.enabled
        elif device == Device.IO:
            return i2c.io.enabled

    async def set_zones_datas_and_update_screen(self, zones_datas: ZoneScreenDto) -> None:
        """Set the zones datas"""
        self.zones_datas = zones_datas
        if not self.is_device_enabled(Device.SCREEN):
            return
        self.screen_device.set_zone_info(zones_datas)
        self.screen_need_update = True

    async def main_loop(self) -> None:
        if self.is_all_i2c_devices_disabled():
            return

        if self.is_device_enabled(Device.TEMPERATURE):
            await self.update_temperature()

        error_counter = 0

        while self.run_loop:
            try:
                if self.loop_iterations == 200 and self.is_device_enabled(Device.TEMPERATURE):
                    await self.update_temperature()
                    await self.screen_device.set_temperature(self.temperature)
                    self.screen_need_update = True
                elif self.screen_need_update:
                    await self.update_screen_if_needed()
                    self.screen_need_update = False
                else:
                    await self.check_io_status()
                self.loop_iterations += 1
                error_counter = 0
                await asyncio.sleep(0.1)
            except OSError:
                if error_counter >= 30:
                    Logs.error(CLASSNAME, "Fail to read/write, abort")
                    raise ReadWriteError()
                await asyncio.sleep(1 * error_counter)
                error_counter += 1

    @staticmethod
    def is_all_i2c_devices_disabled() -> bool:
        """Return true if all i2c devices are disabled"""
        return not any([
            I2C.is_device_enabled(Device.TEMPERATURE),
            I2C.is_device_enabled(Device.IO),
            I2C.is_device_enabled(Device.SCREEN)
        ])

    async def update_temperature(self) -> None:
        """get the temperature datas to the sensor"""
        if not self.is_device_enabled(Device.TEMPERATURE):
            return
        self.temperature = self.temperature_sensor.get_values()
        await WSServer.update_temperature(self.temperature.to_dict())
        self.reset_loop_iterations()

    async def check_io_status(self) -> None:
        """Check io status and perform an action if changed"""
        if not I2C.is_device_enabled(Device.IO) or self.zones_datas is None:
            return

        await self.check_buttons_status()

    async def check_buttons_status(self) -> None:
        """Check if a button is pressed. If so, perform an action."""
        if self.io_device.is_button_pressed(Button.NEXT):
            await self.show_next_vue()
        if self.io_device.is_button_pressed(Button.OK):
            await self.update_zone_state_if_needed()

    async def show_next_vue(self) -> None:
        """update the screen with the next vue and reset the loop_iteration"""
        self.screen_need_update = True
        self.screen_device.show_next_vue()
        self.reset_loop_iterations()

    async def update_zone_state_if_needed(self) -> None:
        """toggle order of the zone selected(if vue is SET_STATE_ZONE(x))"""
        if self.screen_device.get_current_vue() == Vue.SET_STATE_ZONE1:
            await self.toggle_state_zone(ZONE1)
        if self.screen_device.get_current_vue() == Vue.SET_STATE_ZONE2:
            await self.toggle_state_zone(ZONE2)

    async def toggle_state_zone(self, zone_number: int) -> None:
        """toggle state of the zone according to zone_number"""
        if self.toggle_order is not None:
            await self.toggle_order(f"{ZONE}{zone_number}")
        self.reset_loop_iterations()

    async def update_screen_if_needed(self) -> None:
        """update screen vue if screen_need_update is True"""
        if not I2C.is_device_enabled(Device.SCREEN):
            return
        if self.screen_need_update:
            self.screen_device.draw_vue_if_vars_is_not_none()
        if self.screen_device.get_current_vue() != Vue.GENERAL and self.loop_iterations == 100:
            self.screen_device.show_general_vue()

    def stop(self) -> None:
        """Stop event loop"""
        self.run_loop = False

    def reset_loop_iterations(self) -> None:
        """Used to reset the loop_iteration variable"""
        self.loop_iterations = 0

    def start_main_loop(self) -> None:
        """Start the main asyncio loop"""
        self.loop.create_task(self.main_loop())
        threading.Thread(target=self.loop.run_forever).start()
