"""Test frostfree class"""
import time
import unittest
from datetime import datetime
from threading import Thread
from typing import Optional
from unittest.mock import patch, mock_open

from src.localStorage.config.config import Config
from src.localStorage.persistence.dto.persistence_dto import PersistenceDto
from src.localStorage.persistence.persistence import Persistence
from src.shared.enum.state import State
from src.zone.dto.info_frostfree import InfoFrostfree
from src.zone.frostfree import Frostfree
from src.zone.zone import Zone
from test.helpers.fixtures.localStorage.config.config_dto_fixture import config_dto_fixture
from test.helpers.fixtures.localStorage.persistence.persistence_dto_fixture import persistence_dto_fixture

ZONE1 = "zone1"


class TestFrostFree(unittest.TestCase):
    persistence_datas: Optional[PersistenceDto] = None

    def setUp(self):
        TestFrostFree.persistence_datas = persistence_dto_fixture()
        self.open_file = patch('src.localStorage.local_storage.open', self.mock_open_file())
        self.open_file.start()
        self.remove_file = patch('os.remove')
        self.remove_file.start()

        self.config_data = config_dto_fixture()
        self.config_data.network.ip = []
        self.config = patch.object(Config, 'get_config', return_value=self.config_data)
        self.config.start()

        self.thread = None
        self.zone: Optional[Zone] = None
        self.frostfree: Optional[Frostfree] = None

    def tearDown(self) -> None:
        if self.frostfree:
            self.frostfree.timer.stop()
            self.frostfree = None
            self.thread.join()
        if self.zone:
            self.zone.timer.stop()
            self.zone = None
            self.thread.join()

        self.open_file.stop()
        Persistence._initialized = False
        TestFrostFree.persistence_datas = None
        self.remove_file.stop()
        self.config.stop()

    @staticmethod
    def mock_open_file():
        mock_open_obj = mock_open()
        mock_file_handle = mock_open_obj.return_value
        mock_file_handle.read.return_value = TestFrostFree.persistence_datas
        mock_file_handle.write.side_effect = TestFrostFree.write_persistence
        return mock_open_obj

    @staticmethod
    def write_persistence(data):
        TestFrostFree.persistence_datas = data

    def start_thread(self):
        self.thread = Thread(target=self.run_frostfree())
        self.thread.start()
        time.sleep(0.5)

    def run_frostfree(self):
        self.zone = Zone(1)
        time.sleep(0.5)
        self.frostfree = Frostfree([self.zone])

    def test_restore(self):
        Persistence().set_frostfree_end_date(datetime.fromtimestamp(datetime.now().timestamp() + 120))

        self.start_thread()

        self.assertNotEqual(self.frostfree.end_date, None)
        self.assertEqual(self.zone.current_state, State.FROSTFREE)

    def test_restore_end_date_expired(self):
        Persistence().set_frostfree_end_date(datetime.fromtimestamp(datetime.now().timestamp()))

        self.start_thread()

        self.assertEqual(self.frostfree.end_date, None)
        self.assertNotEqual(self.zone.current_state, State.FROSTFREE)

    def test_can_stopped(self):
        Persistence().set_frostfree_end_date(datetime.fromtimestamp(datetime.now().timestamp() + 120))

        self.start_thread()
        self.frostfree.stop()

        self.assertEqual(self.frostfree.end_date, None)
        self.assertNotEqual(self.zone.current_state, State.FROSTFREE)

    def test_get_data(self):
        Persistence().set_frostfree_end_date(datetime.fromtimestamp(datetime.now().timestamp() + 120))
        self.start_thread()
        info_frostfree = InfoFrostfree(self.frostfree.end_date)
        result = self.frostfree.get_data()

        self.assertEqual(info_frostfree, result)


if __name__ == '__main__':
    unittest.main()
