"""GeneralVue Class"""
from PIL import Image

from src.i2c.screen.draw.temperature_elements import TemperatureElements
from src.i2c.screen.draw.zone_elements import ZoneElements
from src.i2c.screen.dto.point_dto import PointDto
from src.i2c.screen.dto.zone_screen_dto import ZoneScreenDto
from src.i2c.screen.vues.vue_impl import VueImpl
from src.i2c.temperature.dto.sensor_dto import SensorDto


class GeneralVue(ZoneElements, TemperatureElements, VueImpl):
    """Draw and return a displayable image for the General vue"""
    def __init__(self, zones_info: ZoneScreenDto, temperature_info: SensorDto):
        super().__init__()
        self.zones_info = zones_info
        self.temperature_info = temperature_info

    def draw_image(self) -> Image:
        self.draw_big_temperature(self.temperature_info.temperature)
        self.draw_humidity(self.temperature_info.humidity, PointDto(45, 35))
        self.draw_zone_state("Z1", self.zones_info.zone1_state, PointDto(25, 50))
        self.draw_zone_state("Z2", self.zones_info.zone2_state, PointDto(75, 50))
        self.draw_menu_next()
