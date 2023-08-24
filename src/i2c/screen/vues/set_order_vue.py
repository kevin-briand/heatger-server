"""SetOrderVue Class"""
from PIL import Image

from src.i2c.screen.draw.global_elements import GlobalElements
from src.i2c.screen.draw.zone_elements import ZoneElements
from src.i2c.screen.dto.point_dto import PointDto
from src.i2c.screen.vues.consts import WHITE
from src.i2c.screen.vues.vue_impl import VueImpl


class SetOrderVue(ZoneElements, GlobalElements, VueImpl):
    """Draw and return a displayable image for the Set_order vue"""
    def __init__(self, zone_name, zone_state):
        super().__init__()
        self.zone_name = zone_name
        self.zone_state = zone_state

    def draw_image(self) -> Image:
        self.draw.text((10, 5), "Switch Order :", fill=WHITE)
        self.draw.text((10, 20), F"Zone {self.zone_name}", fill=WHITE)
        self.draw_state(self.zone_state, PointDto(60, 30))
        self.draw_menu_next()
        self.draw_menu_order()
