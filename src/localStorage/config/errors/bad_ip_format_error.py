"""BadIpFormatError Exception"""
from src.localStorage.config.errors.config_error import ConfigError


class BadIpFormatError(ConfigError):
    """return a BadIpFormatError exception"""

    def __init__(self, ip: str):
        super().__init__(F"Bad ip format ! ({ip})")
