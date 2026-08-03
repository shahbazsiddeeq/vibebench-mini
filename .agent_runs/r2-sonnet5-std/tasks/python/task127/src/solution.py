import threading


class TokenBucket:
    def __init__(self, capacity):
        if capacity < 1:
            raise ValueError("capacity must be >= 1")
        self._capacity = capacity
        self._tokens = capacity
        self._lock = threading.Lock()

    def allow(self, n=1):
        with self._lock:
            if self._tokens >= n:
                self._tokens -= n
                return True
            return False

    def refill(self, n):
        with self._lock:
            self._tokens = min(self._capacity, self._tokens + n)

    @property
    def tokens(self):
        with self._lock:
            return self._tokens
