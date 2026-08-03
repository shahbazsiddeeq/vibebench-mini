import threading
from typing import Any


class TokenBucket:
    """A thread-safe token bucket that starts at full capacity."""

    def __init__(self, capacity: Any) -> None:
        if capacity < 1:
            raise ValueError("capacity must be at least 1")
        self._capacity = capacity
        self._tokens = capacity
        self._lock = threading.Lock()

    @property
    def tokens(self) -> Any:
        """Return the current number of available tokens."""
        with self._lock:
            return self._tokens

    def allow(self, n: Any = 1) -> bool:
        """Atomically consume *n* tokens if enough are available."""
        if n < 0:
            raise ValueError("n must be non-negative")
        with self._lock:
            if self._tokens < n:
                return False
            self._tokens -= n
            return True

    def refill(self, n: Any) -> None:
        """Atomically add *n* tokens, capped at the bucket's capacity."""
        if n < 0:
            raise ValueError("n must be non-negative")
        with self._lock:
            self._tokens = min(self._capacity, self._tokens + n)
