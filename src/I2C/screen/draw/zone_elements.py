"""ZoneElements Class"""
from abc import ABC

from src.I2C.screen.dto.point_dto import PointDto
from src.I2C.screen.vues.consts import WHITE
from src.I2C.screen.vues.vue_impl import VueImpl
from src.shared.enum.orders import Orders


class ZoneElements(VueImpl, ABC):
    """Abstract class regrouping the zone elements to draw"""
    def draw_state(self, state: Orders, position: PointDto) -> None:
        """
        draw a pattern according to state.
        :param state: the current state of the zone
        :param position: the initial position(x, y) to the pattern
        :raise OutOfRangeError: if position is out of range
        """
        self.validate_position(position)
        if state == Orders.COMFORT:
            self.draw.line([(1 + position.x, 6 + position.y), (3 + position.x, 6 + position.y)], fill=WHITE)
            self.draw.line([(9 + position.x, 6 + position.y), (11 + position.x, 6 + position.y)], fill=WHITE)
            self.draw.line([(6 + position.x, 1 + position.y), (6 + position.x, 3 + position.y)], fill=WHITE)
            self.draw.line([(6 + position.x, 9 + position.y), (6 + position.x, 11 + position.y)], fill=WHITE)
            self.draw.ellipse([(3 + position.x, 3 + position.y), (9 + position.x, 9 + position.y)], fill=WHITE)
            self.draw.line([(1 + position.x, 1 + position.y), (3 + position.x, 3 + position.y)], fill=WHITE)
            self.draw.line([(9 + position.x, 9 + position.y), (11 + position.x, 11 + position.y)], fill=WHITE)
            self.draw.line([(9 + position.x, 3 + position.y), (11 + position.x, 1 + position.y)], fill=WHITE)
            self.draw.line([(3 + position.x, 9 + position.y), (1 + position.x, 11 + position.y)], fill=WHITE)
        elif state == Orders.ECO:
            self.draw.arc([(2 + position.x, 2 + position.y), (9 + position.x, 9 + position.y)], fill=WHITE,
                          start=75, end=285)
            self.draw.arc([(3 + position.x, 3 + position.y), (8 + position.x, 8 + position.y)], fill=WHITE,
                          start=90, end=270)
        elif state == Orders.FROSTFREE:
            self.draw.line([(5 + position.x, 0 + position.y), (5 + position.x, 10 + position.y)], fill=WHITE)
            self.draw.line([(0 + position.x, 5 + position.y), (10 + position.x, 5 + position.y)], fill=WHITE)
            self.draw.line([(0 + position.x, 0 + position.y), (10 + position.x, 10 + position.y)], fill=WHITE)
            self.draw.line([(0 + position.x, 10 + position.y), (10 + position.x, 0 + position.y)], fill=WHITE)
            self.draw.line([(3 + position.x, 0 + position.y), (3 + position.x, 2 + position.y),
                            (7 + position.x, 0 + position.y)], fill=WHITE)
            self.draw.line([(3 + position.x, 8 + position.y), (5 + position.x, 10 + position.y),
                            (7 + position.x, 8 + position.y)], fill=WHITE)
            self.draw.line([(2 + position.x, 3 + position.y), (0 + position.x, 5 + position.y),
                            (2 + position.x, 7 + position.y)], fill=WHITE)
            self.draw.line([(8 + position.x, 3 + position.y), (10 + position.x, 5 + position.y),
                            (8 + position.x, 7 + position.y)], fill=WHITE)
            self.draw.line([(2 + position.x, 0 + position.y), (2 + position.x, 2 + position.y),
                            (0 + position.x, 2 + position.y)], fill=WHITE)

    def draw_zone_state(self, name: str, state: Orders, position: PointDto) -> None:
        """
        draw status and zone name.
        :param name: name of the zone
        :param state: state of the zone
        :param position: the initial position(x, y) to the pattern
        :raise OutOfRangeError: if position is out of range
        """
        self.validate_position(position)
        self.draw.text((position.x, position.y), name, fill=WHITE)
        self.draw_state(state, PointDto(position.x + 15, position.y - 1))
