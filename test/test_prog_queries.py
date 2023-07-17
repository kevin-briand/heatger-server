import json
import os
import unittest
import datetime
from typing import Optional
from unittest.mock import patch, mock_open

from faker import Faker
from flask import Flask

from src.localStorage.config import Config
from src.localStorage.dto.config_dto import ConfigDto
from src.localStorage.jsonEncoder.file_encoder import FileEncoder
from src.network.api.config.queries.prog_queries import prog_bp
from src.shared.enum.orders import Orders
from src.zone.dto.horaire_dto import HoraireDto

config_datas = {}


class TestProgQueries(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(prog_bp)
        self.client = self.app.test_client()
        path = os.path.dirname(__file__).split('test')[0]
        self.config_datas: Optional[ConfigDto] = None
        global config_datas
        with open(path + 'config_template.json', 'r') as config:
            config_datas = config.read()

    @staticmethod
    def horaire_fixture():
        fake = Faker()
        return HoraireDto(day=fake.random.randint(0, 6),
                          hour=datetime.time(fake.random.randint(0, 23), fake.random.randint(0, 59), 0),
                          order=Orders.to_order(fake.random.randint(0, Orders.FROSTFREE.value)))

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

    def test_get_prog(self):
        horaire = self.horaire_fixture()
        with patch('src.network.api.config.queries.prog_queries.Config') as mock_config:
            mock_config_instance = mock_config.return_value
            mock_config_instance.get_config.return_value.zone1.prog = [horaire]
            response = self.client.get('/prog/zone1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(HoraireDto.array_to_horaire(json.loads(response.data)), [horaire])

    def test_get_prog_not_found(self):
        with patch('src.localStorage.local_storage.open', self.mock_open_file()):
            response = self.client.get('/prog/zone3')

        self.assertEqual(response.status_code, 404)

    def test_post_prog(self):
        horaire = self.horaire_fixture()

        with patch('src.localStorage.local_storage.open', self.mock_open_file()) as mock_open_file:
            with patch('src.localStorage.local_storage.LocalStorage.write', self.mock_write_config_file):
                request_json = json.dumps([horaire], cls=FileEncoder)

                response = self.client.post('/prog/zone1', data=request_json, mimetype='application/json')

                self.assertEqual(response.status_code, 200)

                self.update_read_file(mock_open_file)
                config = Config().get_config()
                self.assertEqual(config.zone1.prog, [horaire])

    def test_post_prog_not_found(self):
        with patch('src.localStorage.local_storage.open', self.mock_open_file()):
            response = self.client.post('/prog/zone3', json='')

        self.assertEqual(response.status_code, 404)

    def test_delete_prog(self):
        horaire = self.horaire_fixture()

        with patch('src.localStorage.local_storage.open', self.mock_open_file()) as mock_open_file:
            with patch('src.localStorage.local_storage.LocalStorage.write', self.mock_write_config_file):
                config = Config().get_config()
                prog = [horaire]
                config.zone1.prog = prog
                self.mock_write_config_file(config)
                self.update_read_file(mock_open_file)

                response = self.client.delete(f'/prog/zone1/{horaire.to_value()}')
                self.assertEqual(response.status_code, 200)

                self.update_read_file(mock_open_file)
                config = Config().get_config()
                self.assertEqual(config.zone1.prog, [])

    def test_delete_prog_not_found(self):
        horaire = self.horaire_fixture()

        with patch('src.localStorage.local_storage.open', self.mock_open_file()):
            response = self.client.delete(f'/prog/zone3/{horaire.to_value()}')
            self.assertEqual(response.status_code, 404)

            response = self.client.delete(f'/prog/zone1/{horaire.to_value()}')
            self.assertEqual(response.status_code, 404)

    def test_delete_all_prog(self):
        with patch('src.localStorage.local_storage.open', self.mock_open_file()) as mock_open_file:
            with patch('src.localStorage.local_storage.LocalStorage.write', self.mock_write_config_file):
                config = Config().get_config()
                prog = [self.horaire_fixture(), self.horaire_fixture()]
                config.zone1.prog = prog
                self.mock_write_config_file(config)
                self.update_read_file(mock_open_file)

                response = self.client.delete(f'/prog/zone1')
                self.assertEqual(response.status_code, 200)

                self.update_read_file(mock_open_file)
                config = Config().get_config()
                self.assertEqual(config.zone1.prog, [])

    def test_delete_all_prog_not_found(self):
        with patch('src.localStorage.local_storage.open', self.mock_open_file()) as mock_open_file:
            response = self.client.delete(f'/prog/zone3')

        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
