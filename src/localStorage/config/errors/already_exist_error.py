"""AlreadyExistError Exception"""
from src.localStorage.config.errors.config_error import ConfigError


class AlreadyExistError(ConfigError):
    """return a AlreadyExistError exception"""

    def __init__(self, name: str):
        super().__init__(F"{name} already exist !")
