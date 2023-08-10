"""ConfigError Exception"""
from src.localStorage.config.consts import CLASSNAME
from src.shared.logs.logs import Logs


class ConfigError(Exception):
    """return a Config exception"""

    def __init__(self, message: str):
        Logs.error(CLASSNAME, message)
        super().__init__(F"{CLASSNAME}: {message}")
