"""
src/solution.py

A thread-safe, capacity-limited resource pool built on top of the
standard library ``threading`` module only.

The public API is:

    ResourcePool(capacity: int)
        .acquire(timeout: float | None = None) -> bool
        .release() -> None
        .available() -> int
        .slot(timeout: float | None = None) -> context manager

All inputs are validated defensively and no internal state or
implementation detail is ever leaked through exception messages.
"""

from __future__ import annotations

import threading
import time
from contextlib import contextmanager
from typing import Iterator, Optional


class ResourcePool:
    """A simple counting semaphore-like pool with a bounded capacity.

    At any instant, at most ``capacity`` callers may hold a permit that
    has been acquired but not yet released.
    """

    __slots__ = ("_capacity", "_available", "_lock", "_cond")

    def __init__(self, capacity: int) -> None:
        if isinstance(capacity, bool) or not isinstance(capacity, int):
            raise ValueError("capacity must be an integer >= 1")
        if capacity < 1:
            raise ValueError("capacity must be an integer >= 1")

        self._capacity = capacity
        self._available = capacity
        self._lock = threading.Lock()
        self._cond = threading.Condition(self._lock)

    @staticmethod
    def _validate_timeout(timeout: Optional[float]) -> None:
        if timeout is None:
            return
        if isinstance(timeout, bool) or not isinstance(timeout, (int, float)):
            raise ValueError("timeout must be a non-negative number or None")
        if timeout < 0:
            raise ValueError("timeout must be a non-negative number or None")

    def acquire(self, timeout: Optional[float] = None) -> bool:
        """Block until a permit is available, or until timeout elapses.

        Returns True once a permit has been granted, False if the
        timeout elapsed first. timeout=None blocks indefinitely.
        timeout=0 performs a single non-blocking check.
        """
        self._validate_timeout(timeout)

        with self._cond:
            if timeout == 0:
                if self._available > 0:
                    self._available -= 1
                    return True
                return False

            def _has_permit() -> bool:
                return self._available > 0

            granted = self._cond.wait_for(_has_permit, timeout=timeout)
            if granted:
                self._available -= 1
                return True
            return False

    def release(self) -> None:
        """Return one permit to the pool.

        Raises ValueError if this would push availability above the
        configured capacity (i.e. there is no outstanding permit to
        release).
        """
        with self._cond:
            if self._available >= self._capacity:
                raise ValueError(
                    "release() called without a matching acquire(); "
                    "no permits are currently checked out"
                )
            self._available += 1
            self._cond.notify()

    def available(self) -> int:
        """Return how many permits are currently free."""
        with self._lock:
            return self._available

    @contextmanager
    def slot(self, timeout: Optional[float] = None) -> Iterator["ResourcePool"]:
        """Context manager that acquires a permit on enter and releases
        it on exit.

        Raises TimeoutError if a permit cannot be acquired within the
        given timeout.
        """
        self._validate_timeout(timeout)
        acquired = self.acquire(timeout)
        if not acquired:
            raise TimeoutError(
                "timed out waiting to acquire a resource pool slot"
            )
        try:
            yield self
        finally:
            self.release()
