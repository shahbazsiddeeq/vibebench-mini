"""Thread-safe semaphore-style resource pool."""

from __future__ import annotations

import threading
import time
from contextlib import contextmanager
from typing import Iterator


class ResourcePool:
    """A fixed-capacity pool of permits shared between threads."""

    def __init__(self, capacity: int):
        if capacity < 1:
            raise ValueError("capacity must be at least 1")
        self._capacity = capacity
        self._available = capacity
        self._condition = threading.Condition()

    def acquire(self, timeout: float | None = None) -> bool:
        """Acquire a permit, returning False if the timeout expires."""
        with self._condition:
            if timeout is None:
                while self._available == 0:
                    self._condition.wait()
            else:
                deadline = time.monotonic() + timeout
                while self._available == 0:
                    remaining = deadline - time.monotonic()
                    if remaining <= 0:
                        return False
                    self._condition.wait(remaining)

            self._available -= 1
            return True

    def release(self) -> None:
        """Release a permit, raising ValueError if none are checked out."""
        with self._condition:
            if self._available >= self._capacity:
                raise ValueError("cannot release an unacquired permit")
            self._available += 1
            self._condition.notify()

    def available(self) -> int:
        """Return the number of currently available permits."""
        with self._condition:
            return self._available

    @contextmanager
    def slot(self, timeout: float | None = None) -> Iterator[ResourcePool]:
        """Acquire and release a permit around a context block."""
        if not self.acquire(timeout):
            raise TimeoutError("timed out waiting for a resource permit")
        try:
            yield self
        finally:
            self.release()
