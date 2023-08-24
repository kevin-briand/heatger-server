import json
import os.path
import unittest
from unittest.mock import patch, Mock

from src.localStorage.config.config import Config
from src.localStorage.errors.file_not_readable_error import FileNotReadableError
from src.localStorage.jsonEncoder.json_encoder import JsonEncoder
from src.network.api.api import Api
from src.network.api.middleware.middleware import Middleware
from src.network.dto.ip_dto import IpDto
from test.helpers.fixtures.localStorage.config.config_dto_fixture import config_dto_fixture
from test.helpers.fixtures.localStorage.config.ip_dto_fixture import ip_dto_fixture


class TestIpQueries(unittest.TestCase):

    def setUp(self):
        self.app = Api()
        self.client = self.app.application.test_client()
        self.config = config_dto_fixture()
        Config._initialised = False
        self.middleware = patch.object(Middleware, 'check_auth', return_value=True)
        self.middleware.start()
        self.get_config = patch.object(Config, 'get_config', return_value=self.config)
        self.get_config.start()
        self.remove_file = patch('os.remove')
        self.remove_file.start()

    def tearDown(self) -> None:
        self.middleware.stop()
        self.get_config.stop()
        self.remove_file.stop()
        path = os.path.dirname(__file__).split('test')[0]
        if os.path.isfile(path + '/config.json'):
            os.remove(path + '/config.json')

    def test_get_ip(self):
        response = self.client.get('/ip')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(IpDto.array_to_ip_dto(json.loads(response.data)), self.config.network.ip)

    def test_get_ip_raise_api_error_if_cant_get_data(self):
        with patch.object(Config, 'get_config', Mock(side_effect=FileNotReadableError('config.json'))):
            response = self.client.get('/ip')

        self.assertEqual(response.status_code, 400)

    def test_post_ip(self):
        ip = ip_dto_fixture()
        request_json = json.dumps(ip, cls=JsonEncoder)

        response = self.client.post('/ip', data=request_json, mimetype='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(IpDto.array_to_ip_dto(json.loads(response.data)), Config().get_config().network.ip)

    def test_get_ip_raise_empty_data_error_if_no_data_provided(self):
        with patch.object(Config, 'get_config', Mock(side_effect=FileNotReadableError('config.json'))):
            response = self.client.post('/ip', data='[]', mimetype='application/json')

        self.assertEqual(response.status_code, 400)

    def test_add_ip_raise_api_error_if_ip_has_bad_format(self):
        ip = ip_dto_fixture()
        ip.ip = '1251515388'
        request_json = json.dumps(ip, cls=JsonEncoder)

        response = self.client.post('/ip', data=request_json, mimetype='application/json')

        self.assertEqual(response.status_code, 400)

    def test_delete_ip(self):
        ip = self.config.network.ip[0]

        response = self.client.delete(f'/ip/{ip.ip}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(IpDto.array_to_ip_dto(json.loads(response.data)), self.config.network.ip)

    def test_delete_ip_not_found(self):
        ip = ip_dto_fixture()

        response = self.client.delete(f'/ip/{ip.ip}')

        self.assertEqual(response.status_code, 404)

    def test_delete_ip_raise_empty_data_error_if_no_data_provided(self):
        ip = self.config.network.ip[0]

        with patch.object(Config, 'get_config', Mock(side_effect=FileNotReadableError('config.json'))):
            response = self.client.delete(F'/ip/{ip.ip}')

        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
