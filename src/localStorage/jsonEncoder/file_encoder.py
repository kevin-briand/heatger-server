"""FileEncoder class"""
import datetime
from json import JSONEncoder

from src.I2C.dto.device_dto import DeviceDto
from src.shared.enum.state import State


class FileEncoder(JSONEncoder):
    """Serialize objects"""
    def default(self, o):
        if isinstance(o, State):
            return o.value
        if isinstance(o, datetime.time):
            return o.isoformat()
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        if isinstance(o, DeviceDto):
            return o.to_object()
        return o.__dict__
