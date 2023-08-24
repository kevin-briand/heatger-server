"""NotFoundError Exception"""
from src.network.api.errors.api_error import ApiError


class NotFoundError(ApiError):
    """return a NotFoundError exception"""

    def __init__(self, name: str):
        super().__init__(F"{name} not found !", 404)
