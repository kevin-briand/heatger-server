"""object for config file"""
from dataclasses import dataclass


@dataclass
class ApiDto:
    """API data object"""

    # pylint: disable=unused-argument
    def __init__(self, username: str, password: str, *args, **kwargs):
        self.username = username
        self.password = password

    def to_object(self):

        """return an object of this class"""
        return {
            "username": self.username,
            "password": self.password
        }
