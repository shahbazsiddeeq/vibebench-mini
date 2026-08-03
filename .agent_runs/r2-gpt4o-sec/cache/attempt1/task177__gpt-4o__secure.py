import threading
from contextlib import contextmanager
from typing import Optional

class ResourcePool:
    def __init__(self, capacity: int):
        if capacity < 1:
            raise ValueError("Capacity must be at least 1.")
        self._capacity = capacity
        self._lock = threading.Lock()
        self._condition = threading.Condition(self._lock)
        self._available = capacity

    def acquire(self, timeout: Optional[float] = None) -> bool:
        with self._condition:
            if timeout is not None and timeout < 0:
                return False
            if timeout == 0:
                if self._available > 0:
                    self._available -= 1
                    return True
                return False
            else:
                end_time = None if timeout is None else threading.current_thread().time() + timeout
                while self._available == 0:
                    if timeout is not None:
                        remaining = end_time - threading.current_thread().time()
                        if remaining <= 0:
                            return False
                        self._condition.wait(remaining)
                    else:
                        self._condition.wait()
                self._available -= 1
                return True

    def release(self):
        with self._condition:
            if self._available >= self._capacity:
                raise ValueError("Cannot release more than acquired.")
            self._available += 1
            self._condition.notify()

    def available(self) -> int:
        with self._lock:
            return self._available

    @contextmanager
    def slot(self, timeout: Optional[float] = None):
        if not self.acquire(timeout=timeout):
            raise TimeoutError("Could not acquire resource within timeout.")
        try:
            yield
        finally:
            self.release()
