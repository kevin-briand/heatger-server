import threading
from datetime import datetime


class Timer:
    def __init__(self):
        self.time_start = None
        self.timeout = None
        self.timer_thread = None

    def start(self, timeout, on_timeout_callback):
        self.time_start = datetime.now().timestamp()
        self.timeout = timeout
        self.timer_thread = threading.Timer(self.timeout, on_timeout_callback)
        self.timer_thread.start()

    def stop(self):
        if self.timer_thread is None:
            return
        self.timer_thread.cancel()
        self.time_start = None
        self.timeout = None

    def get_remaining_time(self) -> int:
        if self.timeout is None or self.time_start is None:
            return -1
        return int(self.timeout - (datetime.now().timestamp() - self.time_start))