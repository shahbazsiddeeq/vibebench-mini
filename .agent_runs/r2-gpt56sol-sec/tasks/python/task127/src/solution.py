"""Thread-safe token bucket rate limiter."""

from __future__ import annotations

import threading
from numbers import Integral


class TokenBucket:
    """A fixed-capacity, thread-safe token bucket."""

    def __init__(self, capacity: int) -> None:
        if isinstance(capacity, bool) or not isinstance(capacity, Integral):
            raise TypeError("capacity must be an integer")
        if capacity < 1:
            raise ValueError("capacity must be at least 1")

        self._capacity = int(capacity)
        self._tokens = self._capacity
        self._lock = threading.Lock()

    @staticmethod
    def _validate_amount(n: int) -> int:
        if isinstance(n, bool) or not isinstance(n, Integral):
            raise TypeError("token amount must be an integer")
        if n < 0:
            raise ValueError("token amount must be non-negative")
        return int(n)

    def allow(self, n: int = 1) -> bool:
        """Atomically consume *n* tokens if enough are available."""
        amount = self._validate_amount(n)
        with self._lock:
            if self._tokens < amount:
                return False
            self._tokens -= amount
            return True

    def refill(self, n: int) -> None:
        """Atomically add *n* tokens without exceeding capacity."""
        amount = self._validate_amount(n)
        with self._lock:
            self._tokens = min(self._capacity, self._tokens + amount)

    @property
    def tokens(self) -> int:
        """Return the current token count."""
        with self._lock:
            return self._tokens
