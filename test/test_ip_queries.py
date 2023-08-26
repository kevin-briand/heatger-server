import json
import unittest
from unittest.mock import patch, Mock

from src.localStorage.config.config import Config
from src.localStorage.errors.file_not_readable_error import FileNotReadableError
from src.localStorage.jsonEncoder.json_encoder import JsonEncoder
from src.network.dto.ip_dto import IpDto
from test.helpers.fixtures.localStorage.config.ip_dto_fixture import ip_dto_fixture
from test.helpers.patchs.api_patch import ApiPatch
from test.helpers.patchs.config_patch import ConfigPatch


class TestIpQueries(unittest.TestCase):

    def setUp(self):
        self.client = ApiPatch.start_patch(self)
        ApiPatch.start_patch_middleware(self)
        ConfigPatch.start_patch(self)

    def tearDown(self) -> None:
        ApiPatch.stop_patch(self)
        ConfigPatch.stop_patch(self)


    def test_get_ip(self):
        response = self.client.get('/ip')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(IpDto.array_to_ip_dto(json.loads(response.data)), [])

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
        ip = ip_dto_fixture()
        Config().add_ip(ip)
        self.assertEqual(Config().get_config().network.ip, [ip])

        response = self.client.delete(f'/ip/{ip.ip}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(IpDto.array_to_ip_dto(json.loads(response.data)), [])

    def test_delete_ip_not_found(self):
        ip = ip_dto_fixture()

        response = self.client.delete(f'/ip/{ip.ip}')

        self.assertEqual(response.status_code, 404)

    def test_delete_ip_raise_empty_data_error_if_no_data_provided(self):
        ip = ip_dto_fixture()
        Config().add_ip(ip)
        self.assertEqual(Config().get_config().network.ip, [ip])

        with patch.object(Config, 'get_config', Mock(side_effect=FileNotReadableError('config.json'))):
            response = self.client.delete(F'/ip/{ip.ip}')

        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
