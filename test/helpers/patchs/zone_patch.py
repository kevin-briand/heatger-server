from unittest.mock import patch


class ZonePatch:
    @staticmethod
    def start_patch(test):
        test.wait_time_const = patch('src.zone.zone.WAIT_TIME', return_value=1)
        test.wait_time_const.start()
        test.gpio = patch('src.pilot.pilot.Gpio')
        test.gpio.start()

    @staticmethod
    def stop_patch(test):
        test.wait_time_const.stop()
        test.gpio.stop()
