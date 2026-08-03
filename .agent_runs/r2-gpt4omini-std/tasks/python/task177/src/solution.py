import threading
import time

class ResourcePool:
    def __init__(self, capacity: int):
        if capacity < 1:
            raise ValueError("Capacity must be at least 1.")
        self._capacity = capacity
        self._available = capacity
        self._lock = threading.Lock()
        self._condition = threading.Condition(self._lock)

    def acquire(self, timeout: float = None) -> bool:
        with self._condition:
            if timeout is None:
                while self._available == 0:
                    self._condition.wait()
            else:
                end_time = time.time() + timeout
                while self._available == 0:
                    remaining = end_time - time.time()
                    if remaining <= 0:
                        return False
                    self._condition.wait(remaining)

            self._available -= 1
            return True

    def release(self) -> None:
        with self._condition:
            if self._available >= self._capacity:
                raise ValueError("Cannot release more than acquired.")
            self._available += 1
            self._condition.notify()

    def available(self) -> int:
        with self._lock:
            return self._available

    def slot(self, timeout: float = None):
        class Slot:
            def __init__(self, pool, timeout):
                self.pool = pool
                self.timeout = timeout

            def __enter__(self):
                if not self.pool.acquire(timeout):
                    raise TimeoutError("Could not acquire slot within timeout.")

            def __exit__(self, exc_type, exc_val, exc_tb):
                self.pool.release()

        return Slot(self, timeout)
