"""PersistenceError Exception"""
from src.localStorage.persistence.consts import CLASSNAME
from src.shared.logs.logs import Logs


class PersistenceError(Exception):
    """return a Persistence exception"""

    def __init__(self, message: str):
        Logs.error(CLASSNAME, message)
        super().__init__(F"{CLASSNAME}: {message}")
