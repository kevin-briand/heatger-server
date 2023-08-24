"""GlobalElements Class"""
from abc import ABC

from src.i2c.screen.dto.point_dto import PointDto
from src.i2c.screen.vues.consts import WHITE
from src.i2c.screen.vues.vue_impl import VueImpl


class GlobalElements(VueImpl, ABC):
    """Abstract class regrouping common elements to draw"""
    def draw_big_number(self, number: int, position: PointDto, bold=False) -> None:
        """
        draw a big number on the screen
        :param number: number to be drawn
        :param position: the initial position(x, y) to the number
        :param bold: if true, draw two time the number with an offset
        :raise OutOfRangeError: if position is out of range
        """
        self.validate_position(position)
        max_repeat = 2 if bold else 1
        for i in range(max_repeat):
            final_pos = PointDto(position.x + i, position.y + i)
            if number == 0:
                self.draw.line([(0 + final_pos.x, 0 + final_pos.y), (10 + final_pos.x, 0 + final_pos.y),
                                (10 + final_pos.x, 20 + final_pos.y), (0 + final_pos.x, 20 + final_pos.y),
                                (0 + final_pos.x, 0 + final_pos.y)], fill=WHITE)
            if number == 1:
                self.draw.line([(10 + final_pos.x, 0 + final_pos.y), (10 + final_pos.x, 20 + final_pos.y)], fill=WHITE)
            if number == 2:
                self.draw.line([(0 + final_pos.x, 0 + final_pos.y), (10 + final_pos.x, 0 + final_pos.y),
                                (10 + final_pos.x, 10 + final_pos.y), (0 + final_pos.x, 10 + final_pos.y),
                                (0 + final_pos.x, 20 + final_pos.y), (10 + final_pos.x, 20 + final_pos.y)], fill=WHITE)
            if number == 3:
                self.draw.line([(0 + final_pos.x, 0 + final_pos.y), (10 + final_pos.x, 0 + final_pos.y),
                                (10 + final_pos.x, 10 + final_pos.y), (0 + final_pos.x, 10 + final_pos.y),
                                (10 + final_pos.x, 10 + final_pos.y), (10 + final_pos.x, 20 + final_pos.y),
                                (0 + final_pos.x, 20 + final_pos.y)], fill=WHITE)
            if number == 4:
                self.draw.line([(0 + final_pos.x, 0 + final_pos.y), (0 + final_pos.x, 10 + final_pos.y),
                                (10 + final_pos.x, 10 + final_pos.y), (10 + final_pos.x, 0 + final_pos.y),
                                (10 + final_pos.x, 20 + final_pos.y)], fill=WHITE)
            if number == 5:
                self.draw.line([(10 + final_pos.x, 0 + final_pos.y), (0 + final_pos.x, 0 + final_pos.y),
                                (0 + final_pos.x, 10 + final_pos.y), (10 + final_pos.x, 10 + final_pos.y),
                                (10 + final_pos.x, 20 + final_pos.y), (0 + final_pos.x, 20 + final_pos.y)], fill=WHITE)
            if number == 6:
                self.draw.line([(10 + final_pos.x, 0 + final_pos.y), (0 + final_pos.x, 0 + final_pos.y),
                                (0 + final_pos.x, 20 + final_pos.y), (10 + final_pos.x, 20 + final_pos.y),
                                (10 + final_pos.x, 10 + final_pos.y), (0 + final_pos.x, 10 + final_pos.y)], fill=WHITE)
            if number == 7:
                self.draw.line([(0 + final_pos.x, 0 + final_pos.y), (10 + final_pos.x, 0 + final_pos.y),
                                (10 + final_pos.x, 20 + final_pos.y)], fill=WHITE)
            if number == 8:
                self.draw.line([(0 + final_pos.x, 0 + final_pos.y), (10 + final_pos.x, 0 + final_pos.y),
                                (10 + final_pos.x, 20 + final_pos.y), (0 + final_pos.x, 20 + final_pos.y),
                                (0 + final_pos.x, 0 + final_pos.y), (0 + final_pos.x, 10 + final_pos.y),
                                (10 + final_pos.x, 10 + final_pos.y)], fill=WHITE)
            if number == 9:
                self.draw.line([(10 + final_pos.x, 10 + final_pos.y), (0 + final_pos.x, 10 + final_pos.y),
                                (0 + final_pos.x, 0 + final_pos.y),
                                (10 + final_pos.x, 0 + final_pos.y), (10 + final_pos.x, 20 + final_pos.y),
                                (0 + final_pos.x, 20 + final_pos.y)], fill=WHITE)

    def draw_big_point(self, position: PointDto) -> None:
        """
        draw a point on the screen
        :param position: the initial position(x, y) to the point
        :raise OutOfRangeError: if position is out of range
        """
        self.validate_position(position)
        self.draw.line([(0 + position.x, 0 + position.y), (1 + position.x, 0 + position.y),
                        (1 + position.x, 1 + position.y), (0 + position.x, 1 + position.y)], fill=WHITE)

    def draw_menu_next(self) -> None:
        """
        draw a text for the first button on the screen
        """
        self.draw.text((105, 5), "Menu", fill=WHITE)

    def draw_menu_order(self) -> None:
        """
        draw a text for the second button on the screen
        """
        self.draw.text((95, 55), "Order", fill=WHITE)
