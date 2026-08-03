"""Thread-safe count-down latch implementation."""

from __future__ import annotations

import threading


class CountDownLatch:
    """A one-shot synchronization aid that releases waiters at zero."""

    def __init__(self, count: int) -> None:
        if count < 0:
            raise ValueError("count must be non-negative")
        self._count = count
        self._condition = threading.Condition()

    def count_down(self) -> None:
        """Decrement the count, releasing all waiters when it reaches zero."""
        with self._condition:
            if self._count == 0:
                return

            self._count -= 1
            if self._count == 0:
                self._condition.notify_all()

    def await_latch(self, timeout: float | None = None) -> bool:
        """Wait until the count reaches zero or the optional timeout expires."""
        with self._condition:
            return self._condition.wait_for(
                lambda: self._count == 0,
                timeout=timeout,
            )

    def get_count(self) -> int:
        """Return the current count."""
        with self._condition:
            return self._count
