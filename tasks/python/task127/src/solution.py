import threading


class TokenBucket:
    """A thread-safe token bucket rate limiter."""

    def __init__(self, capacity: int):
        if capacity < 1:
            raise ValueError("capacity must be >= 1")
        self._capacity = capacity
        self._tokens = capacity
        self._lock = threading.Lock()

    def allow(self, n: int = 1) -> bool:
        """Atomically consume n tokens if available; return True on success."""
        if n < 0:
            raise ValueError("n must be >= 0")
        with self._lock:
            if self._tokens >= n:
                self._tokens -= n
                return True
            return False

    def refill(self, n: int) -> None:
        """Add n tokens, capped at capacity."""
        if n < 0:
            raise ValueError("n must be >= 0")
        with self._lock:
            self._tokens = min(self._capacity, self._tokens + n)

    @property
    def tokens(self) -> int:
        with self._lock:
            return self._tokens
