"""Timer class"""
import threading
from datetime import datetime


class Timer:
    """Provide a timer"""
    def __init__(self):
        self.time_start = None
        self.timeout = None
        self.timer_thread = None

    def start(self, timeout, on_timeout_callback):
        """start timer with timeout in seconds, on timeout call on_timeout_callback"""
        self.stop()
        self.time_start = datetime.now().timestamp()
        self.timeout = timeout
        self.timer_thread = threading.Timer(self.timeout, on_timeout_callback)
        self.timer_thread.start()

    def stop(self):
        """stop timer"""
        if self.timer_thread is None:
            return
        self.timer_thread.cancel()
        self.time_start = None
        self.timeout = None

    def get_remaining_time(self) -> int:
        """return the remaining time before timeout"""
        if self.timeout is None or self.time_start is None:
            return -1
        return int(self.timeout - (datetime.now().timestamp() - self.time_start))
