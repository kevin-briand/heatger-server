from unittest.mock import patch

from flask.testing import FlaskClient

from src.network.api.api import Api
from src.network.api.middleware.middleware import Middleware


class ApiPatch:

    @classmethod
    def start_patch(cls, test) -> FlaskClient:
        test.app = Api()
        return test.app.application.test_client()

    @classmethod
    def start_patch_middleware(cls, test):
        test.middleware = patch.object(Middleware, 'check_auth', return_value=True)
        test.middleware.start()

    @classmethod
    def stop_patch(cls, test):
        if hasattr(test, 'middleware'):
            test.middleware.stop()
