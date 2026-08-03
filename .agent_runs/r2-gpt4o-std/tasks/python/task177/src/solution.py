import threading
from contextlib import contextmanager
import time

class ResourcePool:
    def __init__(self, capacity: int):
        if capacity < 1:
            raise ValueError("Capacity must be at least 1")
        self.capacity = capacity
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)
        self.available_permits = capacity

    def acquire(self, timeout: float | None = None) -> bool:
        with self.condition:
            end_time = None if timeout is None else time.monotonic() + timeout
            while self.available_permits == 0:
                if timeout is not None:
                    remaining = end_time - time.monotonic()
                    if remaining <= 0:
                        return False
                    self.condition.wait(remaining)
                else:
                    self.condition.wait()
            self.available_permits -= 1
            return True

    def release(self):
        with self.condition:
            if self.available_permits >= self.capacity:
                raise ValueError("Cannot release more permits than capacity")
            self.available_permits += 1
            self.condition.notify()

    def available(self) -> int:
        with self.lock:
            return self.available_permits

    @contextmanager
    def slot(self, timeout: float | None = None):
        if not self.acquire(timeout=timeout):
            raise TimeoutError("Could not acquire a permit within the timeout")
        try:
            yield
        finally:
            self.release()
