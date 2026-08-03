import threading


class CountDownLatch:
    """A one-shot latch that releases waiting threads when its count hits zero."""

    def __init__(self, count):
        if count < 0:
            raise ValueError("count must be non-negative")
        self._count = count
        self._cond = threading.Condition()

    def count_down(self):
        with self._cond:
            if self._count > 0:
                self._count -= 1
                if self._count == 0:
                    self._cond.notify_all()

    def await_latch(self, timeout=None):
        with self._cond:
            if self._count == 0:
                return True
            return self._cond.wait_for(lambda: self._count == 0, timeout)

    def get_count(self):
        with self._cond:
            return self._count
