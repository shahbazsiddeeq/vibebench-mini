import threading
import time

class CountDownLatch:
    def __init__(self, count: int):
        if count < 0:
            raise ValueError("Count cannot be negative")
        self._count = count
        self._condition = threading.Condition()

    def count_down(self):
        with self._condition:
            if self._count > 0:
                self._count -= 1
                if self._count == 0:
                    self._condition.notify_all()

    def await_latch(self, timeout: float | None = None) -> bool:
        with self._condition:
            if self._count == 0:
                return True
            if timeout is None:
                while self._count > 0:
                    self._condition.wait()
                return True
            else:
                end_time = time.monotonic() + timeout
                while self._count > 0:
                    remaining = end_time - time.monotonic()
                    if remaining <= 0:
                        return False
                    self._condition.wait(timeout=remaining)
                return True

    def get_count(self) -> int:
        with self._condition:
            return self._count
