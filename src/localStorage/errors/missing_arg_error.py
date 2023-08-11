"""MissingArgError Exception"""
from src.localStorage.config.consts import CLASSNAME
from src.localStorage.errors.local_storage_error import LocalStorageError


class MissingArgError(LocalStorageError):
    """return a MissingArgError exception"""

    def __init__(self):
        super().__init__("Missing argument in the file", CLASSNAME)
