import json
import unittest
from unittest.mock import patch

from flask import Flask

from src.localStorage.config.config import Config
from src.localStorage.jsonEncoder.json_encoder import JsonEncoder
from src.network.api.config.queries.ip_queries import ip_bp
from src.network.dto.ip_dto import IpDto
from test.helpers.fixtures.localStorage.config.config_dto_fixture import config_dto_fixture
from test.helpers.fixtures.localStorage.config.ip_dto_fixture import ip_dto_fixture

config_datas = {}


class TestIpQueries(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(ip_bp)
        self.client = self.app.test_client()
        self.config = config_dto_fixture()

    def test_get_ip(self):
        with patch.object(Config, 'get_config', return_value=self.config):
            response = self.client.get('/ip')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(IpDto.array_to_ip_dto(json.loads(response.data)), self.config.network.ip)

    def test_post_ip(self):
        ip = ip_dto_fixture()
        request_json = json.dumps(ip, cls=JsonEncoder)

        with patch.object(Config, 'get_config', return_value=self.config):
            response = self.client.post('/ip', data=request_json, mimetype='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(IpDto.array_to_ip_dto(json.loads(response.data)), self.config.network.ip)

    def test_delete_ip(self):
        ip = self.config.network.ip[0]

        with patch.object(Config, 'get_config', return_value=self.config):
            response = self.client.delete(f'/ip/{ip.ip}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(IpDto.array_to_ip_dto(json.loads(response.data)), self.config.network.ip)

    def test_delete_ip_not_found(self):
        ip = ip_dto_fixture()

        with patch.object(Config, 'get_config', return_value=self.config):
            response = self.client.delete(f'/ip/{ip.ip}')

        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
