import json
import unittest
from unittest.mock import patch, Mock

from src.localStorage.config.config import Config
from src.localStorage.errors.local_storage_error import LocalStorageError
from src.localStorage.jsonEncoder.json_encoder import JsonEncoder
from src.zone.dto.schedule_dto import ScheduleDto
from test.helpers.fixtures.zone.schedule_dto_fixture import schedule_dto_fixture
from test.helpers.patchs.api_patch import ApiPatch
from test.helpers.patchs.config_patch import ConfigPatch


class TestProgQueries(unittest.TestCase):

    def setUp(self):
        self.client = ApiPatch.start_patch(self)
        ApiPatch.start_patch_middleware(self)
        ConfigPatch.start_patch(self)
        self.get_config_return_error = patch.object(Config, 'get_config', Mock(side_effect=LocalStorageError('error')))

    def tearDown(self) -> None:
        ApiPatch.stop_patch(self)
        ConfigPatch.stop_patch(self)
        self.get_config_return_error.stop()

    def define_local_storage_should_return_error(self):
        ConfigPatch.stop_patch(self)
        self.get_config_return_error.start()

    def test_get_prog(self):
        response = self.client.get('/prog/zone1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ScheduleDto.from_array(json.loads(response.data)), [])

    def test_get_prog_not_found(self):
        response = self.client.get('/prog/zone3')

        self.assertEqual(response.status_code, 404)

    def test_get_prog_fail_to_get_resources(self):
        self.define_local_storage_should_return_error()
        with patch('src.network.api.config.useCases.prog.prog_request.ProgRequest._ProgRequest__is_zone_exist'):
            response = self.client.get('/prog/zone1')

        self.assertEqual(response.status_code, 400)

    def test_post_prog(self):
        schedule = schedule_dto_fixture()
        request_json = json.dumps([schedule], cls=JsonEncoder)

        response = self.client.post('/prog/zone1', data=request_json, mimetype='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ScheduleDto.from_array(json.loads(response.data)), [schedule])

    def test_post_prog_not_found(self):
        response = self.client.post('/prog/zone3', json='')

        self.assertEqual(response.status_code, 404)

    def test_post_prog_should_return_error_if_no_data_provided(self):
        request_json = json.dumps([], cls=JsonEncoder)

        response = self.client.post('/prog/zone1', data=request_json, mimetype='application/json')

        self.assertEqual(response.status_code, 400)

    def test_post_prog_fail_to_get_resources(self):
        self.define_local_storage_should_return_error()
        schedule = schedule_dto_fixture()
        request_json = json.dumps([schedule], cls=JsonEncoder)

        with patch('src.network.api.config.useCases.prog.prog_request.ProgRequest._ProgRequest__is_zone_exist'):
            response = self.client.post('/prog/zone1', data=request_json, mimetype='application/json')

        self.assertEqual(response.status_code, 400)

    def test_delete_prog(self):
        schedule = schedule_dto_fixture()
        Config().add_schedule('zone1', schedule)
        self.assertEqual(Config().get_config().zone1.prog, [schedule])

        response = self.client.delete(f'/prog/zone1/{schedule.to_value()}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ScheduleDto.from_array(json.loads(response.data)), [])

    def test_delete_prog_not_found(self):
        schedule = schedule_dto_fixture()

        response = self.client.delete(f'/prog/zone3/{schedule.to_value()}')

        self.assertEqual(response.status_code, 404)

        response = self.client.delete(f'/prog/zone1/{schedule.to_value()}')

        self.assertEqual(response.status_code, 404)

    def test_delete_prog_fail_to_get_resources(self):
        self.define_local_storage_should_return_error()
        schedule = schedule_dto_fixture()

        with patch('src.network.api.config.useCases.prog.prog_request.ProgRequest._ProgRequest__is_zone_exist'):
            response = self.client.delete(f'/prog/zone1/{schedule.to_value()}')

        self.assertEqual(response.status_code, 400)

    def test_delete_all_prog(self):
        response = self.client.delete('/prog/zone1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ScheduleDto.from_array(json.loads(response.data)), [])

    def test_delete_all_prog_not_found(self):
        response = self.client.delete('/prog/zone3')

        self.assertEqual(response.status_code, 404)

    def test_delete_all_prog_fail_to_get_resources(self):
        self.define_local_storage_should_return_error()

        with patch('src.network.api.config.useCases.prog.prog_request.ProgRequest._ProgRequest__is_zone_exist'):
            response = self.client.delete('/prog/zone1')

        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
