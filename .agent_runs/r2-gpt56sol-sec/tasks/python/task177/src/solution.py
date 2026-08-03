from __future__ import annotations

import math
import threading
from contextlib import contextmanager
from typing import Iterator


class ResourcePool:
    """A thread-safe pool of a fixed number of resource permits."""

    def __init__(self, capacity: int) -> None:
        if isinstance(capacity, bool) or not isinstance(capacity, int):
            raise TypeError("capacity must be an integer")
        if capacity < 1:
            raise ValueError("capacity must be at least 1")

        self._capacity = capacity
        self._available = capacity
        self._condition = threading.Condition()

    @staticmethod
    def _validate_timeout(timeout: float | None) -> float | None:
        if timeout is None:
            return None
        if isinstance(timeout, bool) or not isinstance(timeout, (int, float)):
            raise TypeError("timeout must be a non-negative number or None")

        value = float(timeout)
        if math.isnan(value) or value < 0:
            raise ValueError("timeout must be non-negative")
        if math.isinf(value):
            return None
        return value

    def acquire(self, timeout: float | None = None) -> bool:
        """Acquire a permit, returning False if the timeout expires."""
        validated_timeout = self._validate_timeout(timeout)

        with self._condition:
            acquired = self._condition.wait_for(
                lambda: self._available > 0,
                timeout=validated_timeout,
            )
            if not acquired:
                return False

            self._available -= 1
            return True

    def release(self) -> None:
        """Return one permit to the pool."""
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
    def slot(self, timeout: float | None = None) -> Iterator[None]:
        """Acquire a permit for the duration of a context."""
        if not self.acquire(timeout=timeout):
            raise TimeoutError("timed out waiting for a resource permit")

        try:
            yield
        finally:
            self.release()
