import json
import os
import unittest
from typing import Optional
from unittest.mock import patch, mock_open

from faker import Faker
from flask import Flask

from src.localStorage.config import Config
from src.localStorage.dto.config_dto import ConfigDto
from src.localStorage.jsonEncoder.file_encoder import FileEncoder
from src.network.api.config.queries.ip_queries import ip_bp
from src.network.dto.ip_dto import IpDto

config_datas = {}


class TestProgQueries(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(ip_bp)
        self.client = self.app.test_client()
        path = os.path.dirname(__file__).split('test')[0]
        self.config_datas: Optional[ConfigDto] = None
        global config_datas
        with open(path + 'config_template.json', 'r') as config:
            config_datas = config.read()

    @staticmethod
    def ip_fixture():
        fake = Faker()
        ip_parts = []
        for _ in range(4):
            ip_parts.append(str(fake.random.randint(0, 255)))
        ip = '.'.join(ip_parts)
        return IpDto(name=fake.name(), ip=ip)

    @staticmethod
    def mock_read_config_file():
        return config_datas

    def mock_write_config_file(self, data):
        global config_datas
        config_datas = json.dumps(data, cls=FileEncoder)

    @staticmethod
    def mock_open_file():
        mock_open_obj = mock_open()
        mock_file_handle = mock_open_obj.return_value
        mock_file_handle.read.return_value = config_datas
        return mock_open_obj

    @staticmethod
    def update_read_file(mock_open_file):
        mock_open_file.return_value.read.return_value = config_datas

    def test_get_ip(self):
        ip = self.ip_fixture()
        with patch('src.network.api.config.queries.ip_queries.Config') as mock_config:
            mock_config_instance = mock_config.return_value
            mock_config_instance.get_config.return_value.network.ip = [ip]
            response = self.client.get('/ip')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(IpDto.array_to_ip_dto(json.loads(response.data)), [ip])

    def test_post_ip(self):
        ip = self.ip_fixture()

        with patch('src.localStorage.local_storage.open', self.mock_open_file()) as mock_open_file:
            with patch('src.localStorage.local_storage.LocalStorage.write', self.mock_write_config_file):
                request_json = json.dumps(ip, cls=FileEncoder)

                response = self.client.post('/ip', data=request_json, mimetype='application/json')

                self.assertEqual(response.status_code, 200)

                self.update_read_file(mock_open_file)
                config = Config().get_config()
                self.assertEqual(config.network.ip, [ip])

    def test_delete_ip(self):
        ip = self.ip_fixture()

        with patch('src.localStorage.local_storage.open', self.mock_open_file()) as mock_open_file:
            with patch('src.localStorage.local_storage.LocalStorage.write', self.mock_write_config_file):
                config = Config().get_config()
                config.network.ip = [ip]
                self.mock_write_config_file(config)
                self.update_read_file(mock_open_file)

                response = self.client.delete(f'/ip/{ip.ip}')
                self.assertEqual(response.status_code, 200)

                self.update_read_file(mock_open_file)
                config = Config().get_config()
                self.assertEqual(config.zone1.prog, [])

    def test_delete_ip_not_found(self):
        ip = self.ip_fixture()

        with patch('src.localStorage.local_storage.open', self.mock_open_file()) as mock_open_file:
            config = Config().get_config()
            config.network.ip = [ip]
            self.mock_write_config_file(config)
            self.update_read_file(mock_open_file)

            response = self.client.delete(f'/ip/{self.ip_fixture().ip}')
            self.assertEqual(response.status_code, 404)

            self.update_read_file(mock_open_file)
            config = Config().get_config()
            self.assertEqual(config.network.ip, [ip])


if __name__ == '__main__':
    unittest.main()
