import contextlib
import threading


class ResourcePool:
    """A counting-semaphore pool that caps concurrent permit holders."""

    def __init__(self, capacity):
        if capacity < 1:
            raise ValueError("capacity must be at least 1")
        self._capacity = capacity
        self._available = capacity
        self._cond = threading.Condition()

    def acquire(self, timeout=None):
        with self._cond:
            if not self._cond.wait_for(lambda: self._available > 0, timeout):
                return False
            self._available -= 1
            return True

    def release(self):
        with self._cond:
            if self._available >= self._capacity:
                raise ValueError("release() called with no permit checked out")
            self._available += 1
            self._cond.notify()

    def available(self):
        with self._cond:
            return self._available

    @contextlib.contextmanager
    def slot(self, timeout=None):
        if not self.acquire(timeout):
            raise TimeoutError("could not acquire a permit in time")
        try:
            yield self
        finally:
            self.release()
