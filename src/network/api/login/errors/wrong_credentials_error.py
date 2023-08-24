"""WrongCredentialsError Exception"""
from src.network.api.errors.api_error import ApiError


class WrongCredentialsError(ApiError):
    """return a WrongCredentialsError exception"""

    def __init__(self):
        super().__init__(F"Wrong username and/or password !", 401)
