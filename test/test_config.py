import json
import unittest
from unittest.mock import mock_open, patch

from src.localStorage.config.config import Config
from src.localStorage.config.errors.config_error import ConfigError
from src.localStorage.jsonEncoder.json_encoder import JsonEncoder
from test.helpers.fixtures.localStorage.config.config_dto_fixture import config_dto_fixture
from test.helpers.fixtures.localStorage.config.ip_dto_fixture import ip_dto_fixture
from test.helpers.fixtures.zone.schedule_dto_fixture import schedule_dto_fixture


class TestConfig(unittest.TestCase):
    config_datas: str = None

    def setUp(self) -> None:
        Config._initialized = False
        self.config = config_dto_fixture()
        TestConfig.config_datas = json.dumps(self.config, cls=JsonEncoder)

    @staticmethod
    def mock_open_file():
        mock_open_obj = mock_open()
        mock_file_handle = mock_open_obj.return_value
        mock_file_handle.read.return_value = TestConfig.config_datas
        return mock_open_obj

    def test_throw_args_error_in_get_config(self):
        Config._initialized = False
        broken_config = self.config
        broken_config.__delattr__('mqtt')
        mock_open_obj = mock_open()
        mock_open_obj.return_value.read.return_value = broken_config

        with patch('src.localStorage.local_storage.open', mock_open_obj):
            with self.assertRaisesRegex(ConfigError, 'missing arguments in the file'):
                Config().get_config()

    def test_add_ip(self):
        new_ip = ip_dto_fixture()

        with patch('src.localStorage.local_storage.open', self.mock_open_file()):
            with patch('os.remove'):
                Config().add_ip(new_ip)
        result = Config().get_config().network.ip

        self.assertIn(new_ip, result)

    def test_throw_bad_ip_format_error_in_add_ip(self):
        bad_ip_format = ip_dto_fixture()
        bad_ip_format.ip = 'badFormat'

        with patch('src.localStorage.local_storage.open', self.mock_open_file()):
            with self.assertRaisesRegex(ConfigError, 'Bad ip format !'):
                Config().add_ip(bad_ip_format)

    def test_throw_exist_ip_error_in_add_ip(self):
        existing_ip = self.config.network.ip[0]
        with patch('src.localStorage.local_storage.open', self.mock_open_file()):
            with self.assertRaisesRegex(ConfigError, 'Ip already exist !'):
                Config().add_ip(existing_ip)

    def test_remove_ip(self):
        ip = self.config.network.ip[0]

        with patch('src.localStorage.local_storage.open', self.mock_open_file()):
            with patch('os.remove'):
                Config().remove_ip(ip)
        result = Config().get_config().network.ip

        self.assertNotIn(ip, result)

    def test_throw_bad_ip_format_error_in_remove_ip(self):
        bad_ip_format = ip_dto_fixture()
        bad_ip_format.ip = 'badFormat'

        with patch('src.localStorage.local_storage.open', self.mock_open_file()):
            with self.assertRaisesRegex(ConfigError, 'Bad ip format !'):
                Config().remove_ip(bad_ip_format)

    def test_add_schedule(self):
        new_schedule = schedule_dto_fixture()

        with patch('src.localStorage.local_storage.open', self.mock_open_file()):
            with patch('os.remove'):
                Config().add_schedule('zone1', new_schedule)
        result = Config().get_config().zone1.prog

        self.assertIn(new_schedule, result)

    def test_throw_bad_schedule_error_in_add_schedule(self):
        bad_schedule = schedule_dto_fixture()
        bad_schedule.day = 8

        with patch('src.localStorage.local_storage.open', self.mock_open_file()):
            with self.assertRaisesRegex(ConfigError, 'schedule is not valid !'):
                Config().add_schedule('zone1', bad_schedule)

    def test_throw_zone_not_found_error_in_add_schedule(self):
        bad_schedule = schedule_dto_fixture()

        with patch('src.localStorage.local_storage.open', self.mock_open_file()):
            with self.assertRaisesRegex(ConfigError, 'Zone not found !'):
                Config().add_schedule('zone3', bad_schedule)

    def test_throw_already_exist_error_in_add_schedule(self):
        existing_schedule = self.config.zone1.prog[0]

        with patch('src.localStorage.local_storage.open', self.mock_open_file()):
            with self.assertRaisesRegex(ConfigError, 'schedule already exist !'):
                Config().add_schedule('zone1', existing_schedule)

    def test_add_schedules(self):
        new_schedules = [schedule_dto_fixture(), schedule_dto_fixture()]

        with patch('src.localStorage.local_storage.open', self.mock_open_file()):
            with patch('os.remove'):
                Config().add_schedules('zone1', new_schedules)
        result = Config().get_config().zone1.prog
        original = self.config.zone1.prog + new_schedules
        original.sort(key=Config._sort_schedule)

        self.assertEqual(result, original)

    def test_throw_zone_not_found_error_in_add_schedules(self):
        bad_schedule = schedule_dto_fixture()

        with patch('src.localStorage.local_storage.open', self.mock_open_file()):
            with self.assertRaisesRegex(ConfigError, 'Zone not found !'):
                Config().add_schedules('zone3', [bad_schedule])

    def test_should_pass_if_schedule_already_exist_in_add_schedules(self):
        schedules = [schedule_dto_fixture(), self.config.zone1.prog[0]]

        with patch('src.localStorage.local_storage.open', self.mock_open_file()):
            with patch('os.remove'):
                Config().add_schedules('zone1', schedules)

        original = [schedules[0]] + self.config.zone1.prog
        original.sort(key=Config._sort_schedule)
        result = Config().get_config().zone1.prog
        self.assertEqual(original, result)

    def test_remove_schedule(self):
        schedule = self.config.zone1.prog[0]

        with patch('src.localStorage.local_storage.open', self.mock_open_file()):
            with patch('os.remove'):
                Config().remove_schedule('zone1', schedule)
        result = Config().get_config().zone1.prog
        self.config.zone1.prog.remove(schedule)
        original = self.config.zone1.prog

        self.assertEqual(result, original)

    def test_throw_bad_schedule_error_in_remove_schedule(self):
        bad_schedule = schedule_dto_fixture()
        bad_schedule.day = 8

        with patch('src.localStorage.local_storage.open', self.mock_open_file()):
            with self.assertRaisesRegex(ConfigError, 'schedule is not valid !'):
                Config().remove_schedule('zone1', bad_schedule)

    def test_throw_zone_not_found_error_in_remove_schedule(self):
        bad_schedule = schedule_dto_fixture()

        with patch('src.localStorage.local_storage.open', self.mock_open_file()):
            with self.assertRaisesRegex(ConfigError, 'Zone not found !'):
                Config().remove_schedule('zone3', bad_schedule)

    def test_remove_all_schedules(self):
        with patch('src.localStorage.local_storage.open', self.mock_open_file()):
            with patch('os.remove'):
                Config().remove_all_schedule('zone1')
        result = Config().get_config().zone1.prog
        original = []

        self.assertEqual(result, original)

    def test_throw_zone_not_found_error_in_remove_all_schedule(self):
        with patch('src.localStorage.local_storage.open', self.mock_open_file()):
            with self.assertRaisesRegex(ConfigError, 'Zone not found !'):
                Config().remove_all_schedule(None)


if __name__ == '__main__':
    unittest.main()
