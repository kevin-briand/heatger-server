"""API Login"""
import json
from uuid import uuid4

from src.localStorage.config.config import Config
from src.localStorage.persistence.persistence import Persistence
from src.network.api.errors.empty_data_error import EmptyDataError
from src.network.api.login.errors.wrong_credentials_error import WrongCredentialsError


class LoginRequest:
    @staticmethod
    def login(data: dict):
        """Login, return a token"""
        if not data:
            raise EmptyDataError()
        api = Config().get_config().api
        if api.username != data['username'] or api.password != data['password']:
            raise WrongCredentialsError()
        Persistence().set_api_token(str(uuid4()))
        return json.dumps(Persistence().get_api_token())
