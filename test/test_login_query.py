import json
import unittest
from unittest.mock import patch, mock_open
from uuid import uuid4

from src.localStorage.config.config import Config
from src.localStorage.jsonEncoder.json_encoder import JsonEncoder
from src.localStorage.persistence.persistence import Persistence
from src.network.api.api import Api
from test.helpers.fixtures.localStorage.config.config_dto_fixture import config_dto_fixture
from test.helpers.fixtures.localStorage.persistence.persistence_dto_fixture import persistence_dto_fixture


class TestLoginQueries(unittest.TestCase):
    persistence_datas: str = None

    def setUp(self):
        self.app = Api()
        self.client = self.app.application.test_client()
        self.config = config_dto_fixture()
        self.persistence = persistence_dto_fixture()
        Config._initialised = False
        TestLoginQueries.persistence_datas = json.dumps(self.persistence, cls=JsonEncoder)
        self.open_file = patch('src.localStorage.local_storage.open', self.mock_open_file())
        self.open_file.start()
        self.get_config = patch.object(Config, 'get_config', return_value=self.config)
        self.get_config.start()
        self.set_token = patch.object(Persistence, 'set_api_token', side_effect=self.set_token)
        self.set_token.start()

    def tearDown(self) -> None:
        self.get_config.stop()
        self.open_file.stop()
        self.set_token.stop()

    @staticmethod
    def mock_open_file():
        mock_open_obj = mock_open()
        mock_file_handle = mock_open_obj.return_value
        mock_file_handle.read.return_value = TestLoginQueries.persistence_datas
        return mock_open_obj

    def set_token(self, token: str):
        self.persistence.api_token = token

    def test_login(self):
        user = json.dumps(self.config.api.__dict__)
        response = self.client.post('/login', data=user, mimetype='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8').strip('"'), Persistence().get_api_token())

    def test_fail_login(self):
        user = '{"username": "admin", "password": ""}'
        response = self.client.post('/login', data=user, mimetype='application/json')

        self.assertEqual(response.status_code, 401)

    def test_fail_login_no_data_provided(self):
        user = '{}'
        response = self.client.post('/login', data=user, mimetype='application/json')

        self.assertEqual(response.status_code, 400)

    def test_fail_login_invalid_token(self):
        response = self.client.get('/ip')

        self.assertEqual(response.status_code, 401)

    def test_login_with_token(self):
        headers = {
            "Authorization": Persistence().get_api_token()
        }
        response = self.client.get('/ip', headers=headers)

        self.assertEqual(response.status_code, 200)

    def test_login_with_bad_token(self):
        headers = {
            "Authorization": uuid4()
        }
        response = self.client.get('/ip', headers=headers)

        self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
