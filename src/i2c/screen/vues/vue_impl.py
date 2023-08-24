"""VueImpl Abstract Class"""
import abc

from PIL import Image, ImageDraw

from src.i2c.screen.consts import MAX_SCREEN_X, MAX_SCREEN_Y, CLASSNAME
from src.i2c.screen.dto.point_dto import PointDto
from src.i2c.screen.vues.consts import BACKGROUND_COLOR, WHITE
from src.shared.errors.out_of_range_error import OutOfRangeError


class VueImpl(metaclass=abc.ABCMeta):
    """Draw and return a displayable image"""
    def __init__(self):
        self.img = Image.new("1", (MAX_SCREEN_X, MAX_SCREEN_Y), BACKGROUND_COLOR)
        self.draw = ImageDraw.Draw(self.img)

    def render(self) -> Image:
        """draw and return an image, if failed, return an error image"""
        try:
            self.draw_image()
            return self.img
        except OutOfRangeError:
            return self.draw_out_of_range_error()

    @staticmethod
    def validate_position(position: PointDto) -> None:
        """
        raise an OutOfRangeError if position is not in screen range
        :param position: the initial position(x, y) to the test
        :raise OutOfRangeError: if position is out of range
        """
        if not 0 < position.x < MAX_SCREEN_X or not 0 < position.y < MAX_SCREEN_Y:
            raise OutOfRangeError(CLASSNAME, "position")

    def draw_out_of_range_error(self) -> Image:
        """
        return an image with the printed error
        """
        self.draw.text((0, 0), "Error : out of range", fill=WHITE)
        return self.img

    @abc.abstractmethod
    def draw_image(self):
        """
        draw and return an image
        :raise OutOfRangeError: if position is out of range
        """
        raise NotImplementedError
