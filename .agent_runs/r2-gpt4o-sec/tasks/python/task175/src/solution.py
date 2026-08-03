import threading
from typing import Optional

class CountDownLatch:
    def __init__(self, count: int):
        if count < 0:
            raise ValueError("Count cannot be negative")
        self._count = count
        self._lock = threading.Lock()
        self._condition = threading.Condition(self._lock)

    def count_down(self):
        with self._lock:
            if self._count > 0:
                self._count -= 1
                if self._count == 0:
                    self._condition.notify_all()

    def await_latch(self, timeout: Optional[float] = None) -> bool:
        with self._lock:
            if self._count == 0:
                return True
            return self._condition.wait_for(lambda: self._count == 0, timeout)

    def get_count(self) -> int:
        with self._lock:
            return self._count
