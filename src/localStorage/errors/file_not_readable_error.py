"""FileNotReadableError Exception"""
from src.localStorage.errors.local_storage_error import LocalStorageError


class FileNotReadableError(LocalStorageError):
    """return a FileNotReadableError exception"""

    def __init__(self, filename: str):
        super().__init__(F"file {filename} not readable !")
