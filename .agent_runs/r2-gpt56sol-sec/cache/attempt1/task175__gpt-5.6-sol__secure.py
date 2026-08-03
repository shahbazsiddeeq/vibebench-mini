"""Thread-safe count-down latch implementation."""

from __future__ import annotations

import math
import threading
import time


class CountDownLatch:
    """A one-shot synchronization primitive released when its count reaches zero."""

    def __init__(self, count: int) -> None:
        if not isinstance(count, int) or isinstance(count, bool):
            raise TypeError("count must be an integer")
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
        """Wait for the count to reach zero, optionally subject to a timeout."""
        if timeout is not None:
            if (
                not isinstance(timeout, (int, float))
                or isinstance(timeout, bool)
            ):
                raise TypeError("timeout must be a number or None")

            timeout = float(timeout)
            if math.isnan(timeout):
                raise ValueError("timeout must not be NaN")

        with self._condition:
            if self._count == 0:
                return True

            if timeout is None or timeout == math.inf:
                while self._count > 0:
                    self._condition.wait()
                return True

            if timeout <= 0:
                return False

            deadline = time.monotonic() + timeout
            while self._count > 0:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    return False
                self._condition.wait(remaining)

            return True

    def get_count(self) -> int:
        """Return the current count."""
        with self._condition:
            return self._count
