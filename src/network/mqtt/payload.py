"""Payload interface"""
import abc


class Payload(metaclass=abc.ABCMeta):
    """abstract class for define sensor payload"""
    @abc.abstractmethod
    def sensor_payload(self, name: str, unit_of_measurement=''):
        """Return an object necessary to define a new sensor"""
        raise NotImplementedError
