"""Payload interface"""
import abc


class GenericConfigDto(metaclass=abc.ABCMeta):
    """abstract class for define sensor/button payload"""
    @abc.abstractmethod
    def payload(self):
        """Return an object necessary to define a new sensor/button"""
        raise NotImplementedError

    @abc.abstractmethod
    def to_object(self):
        """Return an object necessary to define a new sensor/button"""
        raise NotImplementedError
