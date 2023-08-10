import json
import unittest
from unittest.mock import patch

from flask import Flask

from src.localStorage.config.config import Config
from src.localStorage.config.config import ConfigDto
from src.localStorage.jsonEncoder.json_encoder import JsonEncoder
from src.network.api.config.queries.prog_queries import prog_bp
from src.zone.dto.schedule_dto import ScheduleDto
from test.helpers.fixtures.localStorage.config.config_dto_fixture import config_dto_fixture
from test.helpers.fixtures.zone.schedule_dto_fixture import schedule_dto_fixture

config_datas = {}


class TestProgQueries(unittest.TestCase):
    config: ConfigDto = None

    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(prog_bp)
        self.client = self.app.test_client()
        self.config = config_dto_fixture()

    def test_get_prog(self):
        with patch.object(Config, 'get_config', return_value=self.config):
            response = self.client.get('/prog/zone1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ScheduleDto.from_array(json.loads(response.data)), self.config.zone1.prog)

    def test_get_prog_not_found(self):
        with patch.object(Config, 'get_config', return_value=self.config):
            response = self.client.get('/prog/zone3')

        self.assertEqual(response.status_code, 404)

    def test_post_prog(self):
        schedule = schedule_dto_fixture()
        request_json = json.dumps([schedule], cls=JsonEncoder)

        with patch.object(Config, 'get_config', return_value=self.config):
            response = self.client.post('/prog/zone1', data=request_json, mimetype='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ScheduleDto.from_array(json.loads(response.data)), self.config.zone1.prog)

    def test_post_prog_not_found(self):
        with patch.object(Config, 'get_config', return_value=self.config):
            response = self.client.post('/prog/zone3', json='')

        self.assertEqual(response.status_code, 404)

    def test_delete_prog(self):
        schedule = self.config.zone1.prog[0]

        with patch.object(Config, 'get_config', return_value=self.config):
            response = self.client.delete(f'/prog/zone1/{schedule.to_value()}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ScheduleDto.from_array(json.loads(response.data)), self.config.zone1.prog)

    def test_delete_prog_not_found(self):
        schedule = schedule_dto_fixture()

        with patch.object(Config, 'get_config', return_value=self.config):
            response = self.client.delete(f'/prog/zone3/{schedule.to_value()}')

            self.assertEqual(response.status_code, 404)

            response = self.client.delete(f'/prog/zone1/{schedule.to_value()}')

            self.assertEqual(response.status_code, 404)

    def test_delete_all_prog(self):
        with patch.object(Config, 'get_config', return_value=self.config):
            response = self.client.delete(f'/prog/zone1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ScheduleDto.from_array(json.loads(response.data)), [])

    def test_delete_all_prog_not_found(self):
        with patch.object(Config, 'get_config', return_value=self.config):
            response = self.client.delete(f'/prog/zone3')

        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
