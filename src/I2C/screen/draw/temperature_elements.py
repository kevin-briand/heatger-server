"""GlobalElements Class"""
from abc import ABC

from src.I2C.screen.draw.global_elements import GlobalElements
from src.I2C.screen.dto.point_dto import PointDto
from src.I2C.screen.vues.consts import INTEGER, DECIMAL, WHITE
from src.I2C.screen.vues.vue_impl import VueImpl


class TemperatureElements(GlobalElements, VueImpl, ABC):
    """Abstract class regrouping the temperature elements to draw"""
    def draw_big_temperature(self, temperature: float) -> None:
        """
        draw a big temperature on the screen
        :param temperature: the temperature value to draw
        """
        current_temperature = str(temperature)
        split_comma_temp = current_temperature.split('.')
        unity_pos = 0
        if current_temperature.find('.') != -1:
            self.draw_big_number(int(split_comma_temp[INTEGER][0]), PointDto(31, 12), True)
            unity_pos = 1
        self.draw_big_number(int(split_comma_temp[INTEGER][unity_pos]), PointDto(46, 12), True)
        self.draw_big_point(PointDto(60, 32))
        self.draw_big_number(int(split_comma_temp[DECIMAL][0]), PointDto(65, 12), True)
        self.draw.text((80, 12), "°C", fill=WHITE)

    def draw_humidity(self, humidity: int, position: PointDto) -> None:
        """
        draw a humidity on the screen
        :param humidity: the humidity value to draw
        :param position: the initial position(x, y) to the text
        :raise OutOfRangeError: if position is out of range
        """
        self.validate_position(position)
        text_length = self.draw.textlength(str(humidity))
        self.draw.text((0 + position.x, 0 + position.y), str(humidity), fill=WHITE)
        self.draw.text((text_length + position.x, 0 + position.y), "%", fill=WHITE)
