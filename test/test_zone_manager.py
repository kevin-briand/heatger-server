"""Test TestManager class"""
import time
import unittest
from datetime import datetime
from typing import Optional
from unittest.mock import patch, mock_open, Mock

import sys

from paho.mqtt.client import MQTTMessage

from src.network.mqtt.homeAssistant.consts import BUTTON_FROSTFREE, SWITCH_MODE, SWITCH_STATE
from src.shared.enum.mode import Mode
from src.shared.enum.state import State
from src.zone.consts import ZONE
from test.helpers.fixtures.zone.schedule_dto_fixture import schedule_dto_fixture

sys.modules['src.i2c.i2c'] = Mock()

from src.localStorage.config.config import Config
from src.localStorage.persistence.dto.persistence_dto import PersistenceDto
from src.localStorage.persistence.persistence import Persistence
from src.zone.zone_manager import ZoneManager
from test.helpers.fixtures.localStorage.config.config_dto_fixture import config_dto_fixture
from test.helpers.fixtures.localStorage.persistence.persistence_dto_fixture import persistence_dto_fixture


class TestManager(unittest.TestCase):
    persistence_datas: Optional[PersistenceDto] = None

    def setUp(self):
        TestManager.persistence_datas = persistence_dto_fixture()
        self.open_file = patch('src.localStorage.local_storage.open', self.mock_open_file())
        self.open_file.start()
        self.remove_file = patch('os.remove')
        self.remove_file.start()
        self.mqtt = patch('src.network.network.HomeAssistant')
        self.mqtt.start()

        self.config_data = config_dto_fixture()
        self.config_data.network.ip = []
        self.config_data.i2c.enabled = False
        self.config = patch.object(Config, 'get_config', return_value=self.config_data)
        self.config.start()

        self.manager: Optional[ZoneManager] = None

    def tearDown(self) -> None:
        time.sleep(0.5)
        if self.manager.frostfree:
            self.manager.frostfree.timer.stop()
        for zone in self.manager.zones:
            if zone.ping.is_running():
                zone.ping.stop()
                zone.ping.join()
            zone.timer.stop()
        self.manager.stop_datas_loop()
        self.manager.join()
        self.open_file.stop()
        Persistence._initialized = False
        TestManager.persistence_datas = None
        self.remove_file.stop()
        self.mqtt.stop()
        self.config.stop()

    @staticmethod
    def mock_open_file():
        mock_open_obj = mock_open()
        mock_file_handle = mock_open_obj.return_value
        mock_file_handle.read.return_value = TestManager.persistence_datas
        mock_file_handle.write.side_effect = TestManager.write_persistence
        return mock_open_obj

    @staticmethod
    def write_persistence(data):
        TestManager.persistence_datas = data

    def run_manager(self):
        self.manager = ZoneManager()
        self.manager.start()
        time.sleep(0.5)

    @staticmethod
    def create_mqtt_message(topic: str, payload: str = '') -> MQTTMessage:
        mqtt_message: MQTTMessage = MQTTMessage(topic=topic.encode('utf-8'))
        mqtt_message.payload = payload.encode('utf-8')
        return mqtt_message

    def test_init(self):
        self.run_manager()

        self.assertEqual(len(self.manager.zones), 2)
        self.assertNotEqual(self.manager.frostfree, None)

    def test_mqtt_activate_frostfree(self):
        end_date = datetime.fromtimestamp(datetime.now().timestamp() + 60).strftime('%Y-%m-%dT%H:%M')
        mqtt_message: MQTTMessage = self.create_mqtt_message(BUTTON_FROSTFREE, end_date)

        self.run_manager()
        self.manager.on_mqtt_message(mqtt_message)

        self.assertEqual(self.manager.zones[0].current_state, State.FROSTFREE)

    def test_mqtt_deactivate_frostfree(self):
        end_date = datetime.fromtimestamp(datetime.now().timestamp() + 60).strftime('%Y-%m-%dT%H:%M')
        mqtt_activate_message = self.create_mqtt_message(BUTTON_FROSTFREE, end_date)
        mqtt_deactivate_message = self.create_mqtt_message(BUTTON_FROSTFREE, datetime.now().strftime('%Y-%m-%dT%H:%M'))

        self.run_manager()
        self.manager.on_mqtt_message(mqtt_activate_message)
        self.manager.on_mqtt_message(mqtt_deactivate_message)

        self.assertNotEqual(self.manager.zones[0].current_state, State.FROSTFREE)

    def test_mqtt_frostfree_should_do_nothing_if_payload_is_not_correct(self):
        empty_payload: MQTTMessage = self.create_mqtt_message(BUTTON_FROSTFREE)
        bad_format_payload: MQTTMessage = self.create_mqtt_message(BUTTON_FROSTFREE, '25-25-32 21:00')

        self.run_manager()
        self.manager.on_mqtt_message(empty_payload)
        self.assertNotEqual(self.manager.zones[0].current_state, State.FROSTFREE)

        self.manager.on_mqtt_message(bad_format_payload)
        self.assertNotEqual(self.manager.zones[0].current_state, State.FROSTFREE)

    def test_mqtt_switch_mode(self):
        mqtt_message = self.create_mqtt_message(F'{ZONE}1_{SWITCH_MODE}')

        self.run_manager()
        self.manager.on_mqtt_message(mqtt_message)

        self.assertEqual(self.manager.zones[0].current_mode, Mode.MANUAL)

    def test_mqtt_switch_do_nothing_if_zone_number_is_unknown(self):
        mqtt_message = self.create_mqtt_message(F'{ZONE}0_{SWITCH_MODE}')

        self.run_manager()
        self.manager.on_mqtt_message(mqtt_message)

        self.assertEqual(self.manager.zones[0].current_mode, Mode.AUTO)

    def test_mqtt_switch_state(self):
        self.config_data.zone1.prog = [schedule_dto_fixture(State.COMFORT)]
        mqtt_message = self.create_mqtt_message(F'{ZONE}1_{SWITCH_STATE}')

        self.run_manager()
        self.manager.on_mqtt_message(mqtt_message)

        self.assertEqual(self.manager.zones[0].current_state, State.COMFORT)


if __name__ == '__main__':
    unittest.main()
