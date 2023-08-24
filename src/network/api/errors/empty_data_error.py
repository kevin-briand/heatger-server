"""EmptyDataError Exception"""
from src.network.api.errors.api_error import ApiError


class EmptyDataError(ApiError):
    """return a EmptyDataError exception"""

    def __init__(self):
        super().__init__("No data provided !", 400)
