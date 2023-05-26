import abc


class Payload(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def sensor_payload(self, name: str, unit_of_measurement=''):
        raise NotImplementedError
