import threading
from contextlib import contextmanager


class ResourcePool:
    def __init__(self, capacity: int):
        if capacity < 1:
            raise ValueError("capacity must be >= 1")
        self._capacity = capacity
        self._available = capacity
        self._lock = threading.Lock()
        self._cond = threading.Condition(self._lock)

    def acquire(self, timeout: float | None = None) -> bool:
        with self._cond:
            if self._available > 0:
                self._available -= 1
                return True
            if timeout == 0:
                return False
            result = self._cond.wait_for(lambda: self._available > 0, timeout=timeout)
            if result:
                self._available -= 1
                return True
            return False

    def release(self) -> None:
        with self._cond:
            if self._available >= self._capacity:
                raise ValueError("release() called too many times")
            self._available += 1
            self._cond.notify()

    def available(self) -> int:
        with self._lock:
            return self._available

    @contextmanager
    def slot(self, timeout: float | None = None):
        acquired = self.acquire(timeout=timeout)
        if not acquired:
            raise TimeoutError("timed out waiting for resource pool slot")
        try:
            yield self
        finally:
            self.release()
