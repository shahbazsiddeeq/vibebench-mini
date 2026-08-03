import threading


class CountDownLatch:
    def __init__(self, count: int):
        if count < 0:
            raise ValueError("count must be >= 0")
        self._count = count
        self._condition = threading.Condition()

    def count_down(self) -> None:
        with self._condition:
            if self._count > 0:
                self._count -= 1
                if self._count == 0:
                    self._condition.notify_all()

    def await_latch(self, timeout: float = None) -> bool:
        with self._condition:
            if self._count == 0:
                return True
            return self._condition.wait_for(lambda: self._count == 0, timeout=timeout)

    def get_count(self) -> int:
        with self._condition:
            return self._count
