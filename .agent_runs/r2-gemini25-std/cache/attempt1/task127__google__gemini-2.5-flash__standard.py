import threading

class TokenBucket:
    def __init__(self, capacity):
        if capacity < 1:
            raise ValueError("Capacity must be at least 1")
        self._capacity = capacity
        self._tokens = capacity
        self._lock = threading.Lock()

    @property
    def tokens(self):
        with self._lock:
            return self._tokens

    def allow(self, n=1):
        if n < 0:
            raise ValueError("Number of tokens to consume must be non-negative")
        if n == 0:
            return True

        with self._lock:
            if self._tokens >= n:
                self._tokens -= n
                return True
            return False

    def refill(self, n):
        if n < 0:
            raise ValueError("Number of tokens to refill must be non-negative")
        with self._lock:
            self._tokens = min(self._capacity, self._tokens + n)
