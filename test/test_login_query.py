import json
import unittest
from uuid import uuid4

from src.localStorage.config.config import Config
from src.localStorage.persistence.persistence import Persistence
from test.helpers.patchs.api_patch import ApiPatch
from test.helpers.patchs.config_patch import ConfigPatch
from test.helpers.patchs.persistence_patch import PersistencePatch


class TestLoginQueries(unittest.TestCase):
    persistence_datas: str = None

    def setUp(self):
        self.client = ApiPatch.start_patch(self)
        PersistencePatch.start_patch(self)
        ConfigPatch.start_patch(self)

    def tearDown(self) -> None:
        ApiPatch.stop_patch(self)
        PersistencePatch.stop_patch(self)
        ConfigPatch.stop_patch(self)

    def test_login(self):
        user = json.dumps(Config().get_config().api.__dict__)
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
