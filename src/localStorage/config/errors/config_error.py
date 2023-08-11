"""ConfigError Exception"""
from src.localStorage.config.consts import CLASSNAME
from src.localStorage.errors.local_storage_error import LocalStorageError


class ConfigError(LocalStorageError):
    """return a Config exception"""

    def __init__(self, message: str):
        super().__init__(message, CLASSNAME)
