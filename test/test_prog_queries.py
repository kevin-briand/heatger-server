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
from src.shared.enum.state import State
from src.zone.dto.schedule_dto import ScheduleDto

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
    def schedule_fixture():
        fake = Faker()
        return ScheduleDto(day=fake.random.randint(0, 6),
                           hour=datetime.time(fake.random.randint(0, 23), fake.random.randint(0, 59), 0),
                           state=State.to_state(fake.random.randint(0, State.FROSTFREE.value)))

    @staticmethod
    def mock_open_file():
        mock_open_obj = mock_open()
        mock_file_handle = mock_open_obj.return_value
        mock_file_handle.read.return_value = config_datas
        return mock_open_obj

    def write_prog_in_config(self, prog: list[ScheduleDto]):
        with patch('src.localStorage.local_storage.open', self.mock_open_file()):
            with patch('os.remove'):
                config = Config().get_config()
                config.zone1.prog = prog
                Config().write(config)

    def test_get_prog(self):
        schedule = self.schedule_fixture()
        self.write_prog_in_config([schedule])

        response = self.client.get('/prog/zone1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ScheduleDto.from_array(json.loads(response.data)), [schedule])

    def test_get_prog_not_found(self):
        with patch('src.localStorage.local_storage.open', self.mock_open_file()):
            response = self.client.get('/prog/zone3')

        self.assertEqual(response.status_code, 404)

    def test_post_prog(self):
        schedule = self.schedule_fixture()
        self.write_prog_in_config([])

        request_json = json.dumps([schedule], cls=FileEncoder)
        response = self.client.post('/prog/zone1', data=request_json, mimetype='application/json')

        self.assertEqual(response.status_code, 200)

        config = Config().get_config()
        self.assertEqual(config.zone1.prog, [schedule])

    def test_post_prog_not_found(self):
        with patch('src.localStorage.local_storage.open', self.mock_open_file()):
            response = self.client.post('/prog/zone3', json='')

        self.assertEqual(response.status_code, 404)

    def test_delete_prog(self):
        schedule = self.schedule_fixture()
        self.write_prog_in_config([schedule])

        response = self.client.delete(f'/prog/zone1/{schedule.to_value()}')
        self.assertEqual(response.status_code, 200)

        config = Config().get_config()
        self.assertEqual(config.zone1.prog, [])

    def test_delete_prog_not_found(self):
        schedule = self.schedule_fixture()

        with patch('src.localStorage.local_storage.open', self.mock_open_file()):
            response = self.client.delete(f'/prog/zone3/{schedule.to_value()}')
            self.assertEqual(response.status_code, 404)

            response = self.client.delete(f'/prog/zone1/{schedule.to_value()}')
            self.assertEqual(response.status_code, 404)

    def test_delete_all_prog(self):
        self.write_prog_in_config([self.schedule_fixture(), self.schedule_fixture()])

        response = self.client.delete(f'/prog/zone1')
        self.assertEqual(response.status_code, 200)

        config = Config().get_config()
        self.assertEqual(config.zone1.prog, [])

    def test_delete_all_prog_not_found(self):
        with patch('src.localStorage.local_storage.open', self.mock_open_file()):
            response = self.client.delete(f'/prog/zone3')

        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
