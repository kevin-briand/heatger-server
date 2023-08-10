import datetime
import json
import unittest
from unittest.mock import mock_open, patch

from faker import Faker

from src.localStorage.jsonEncoder.json_encoder import JsonEncoder
from src.localStorage.persistence.persistence import Persistence
from src.shared.enum.mode import Mode
from src.shared.enum.state import State
from src.zone.dto.zone_persistence_dto import ZonePersistenceDto
from test.helpers.fixtures.localStorage.persistence.persistence_dto_fixture import persistence_dto_fixture

ZONE_ID = "zone1"
BAD_ZONE_ID = "zone3"


class TestPersistence(unittest.TestCase):
    persistence_datas: str = None

    def setUp(self) -> None:
        Persistence._initialized = False
        self.persistence = persistence_dto_fixture()
        TestPersistence.persistence_datas = json.dumps(self.persistence, cls=JsonEncoder)

    @staticmethod
    def mock_open_file():
        mock_open_obj = mock_open()
        mock_file_handle = mock_open_obj.return_value
        mock_file_handle.read.return_value = TestPersistence.persistence_datas
        return mock_open_obj

    def test_get_state(self):
        with patch('src.localStorage.local_storage.open', self.mock_open_file()):
            state = Persistence().get_state(ZONE_ID)

        self.assertEqual(State.ECO, state)

    def test_set_state(self):
        state = State.COMFORT

        with patch('src.localStorage.local_storage.open', self.mock_open_file()):
            with patch('os.remove'):
                Persistence().set_state(ZONE_ID, state)
        result = Persistence().persist.zones[0].state

        self.assertEqual(result, state)

    def test_get_mode(self):
        with patch('src.localStorage.local_storage.open', self.mock_open_file()):
                mode = Persistence().get_mode(ZONE_ID)

        self.assertEqual(Mode.AUTO, mode)

    def test_set_mode(self):
        mode = Mode.MANUAL

        with patch('src.localStorage.local_storage.open', self.mock_open_file()):
            with patch('os.remove'):
                Persistence().set_mode(ZONE_ID, mode)
        result = Persistence().persist.zones[0].mode

        self.assertEqual(result, mode)

    def test_get_api_token(self):
        with patch('src.localStorage.local_storage.open', self.mock_open_file()):
            token = Persistence().get_api_token()
        result = self.persistence.api_token

        self.assertEqual(result, token)

    def test_set_api_token(self):
        token = Faker().uuid4()

        with patch('src.localStorage.local_storage.open', self.mock_open_file()):
            with patch('os.remove'):
                Persistence().set_api_token(token)
            result = Persistence().persist.api_token

        self.assertEqual(result, token)

    def test_get_frostfree_end_date(self):
        with patch('src.localStorage.local_storage.open', self.mock_open_file()):
            end_date = Persistence().get_frostfree_end_date()
        result = self.persistence.frost_free

        self.assertEqual(result, end_date)

    def test_set_frostfree_end_date(self):
        end_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

        with patch('src.localStorage.local_storage.open', self.mock_open_file()):
            with patch('os.remove'):
                Persistence().set_frostfree_end_date(end_date)
            result = Persistence().persist.frost_free

        self.assertEqual(result, end_date)

    def test_persistence_file_not_exist(self):
        Persistence._initialised = False
        mock_open_obj = mock_open()
        mock_file_handle = mock_open_obj.return_value
        mock_file_handle.read.return_value = ''

        with patch('src.localStorage.local_storage.open', mock_open_obj()):
            with patch('os.remove'):
                Persistence()

        self.assertEqual(len(Persistence().persist.zones), 0)

    def test_get_state_shoud_return_new_zone_if_unknown_zone_id(self):
        state = State.COMFORT
        zone = ZonePersistenceDto(BAD_ZONE_ID, state, Mode.AUTO)

        with patch('src.localStorage.local_storage.open', self.mock_open_file()):
            with patch('os.remove'):
                Persistence().set_state(BAD_ZONE_ID, state)

        self.assertEqual(len(Persistence().persist.zones), 2)
        self.assertIn(zone, Persistence().persist.zones)


if __name__ == '__main__':
    unittest.main()
