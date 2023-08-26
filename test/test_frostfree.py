"""Test frostfree class"""
import time
import unittest
from datetime import datetime
from threading import Thread
from typing import Optional

from src.localStorage.persistence.persistence import Persistence
from src.shared.enum.state import State
from src.zone.dto.info_frostfree import InfoFrostfree
from src.zone.frostfree import Frostfree
from src.zone.zone import Zone
from test.helpers.patchs.config_patch import ConfigPatch
from test.helpers.patchs.persistence_patch import PersistencePatch
from test.helpers.patchs.zone_patch import ZonePatch

ZONE1 = "zone1"


class TestFrostFree(unittest.TestCase):

    def setUp(self):
        ZonePatch.start_patch(self)
        PersistencePatch.start_patch(self)
        ConfigPatch.start_patch(self)

        self.thread = None
        self.zone: Optional[Zone] = None
        self.frostfree: Optional[Frostfree] = None

    def tearDown(self) -> None:
        ZonePatch.stop_patch(self)
        if self.frostfree:
            self.frostfree.stop_loop()
        if self.zone:
            self.zone.stop_loop()
        if self.thread:
            self.thread.join()

        PersistencePatch.stop_patch(self)
        ConfigPatch.stop_patch(self)

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
