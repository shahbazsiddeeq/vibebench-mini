import threading

class TokenBucket:
    def __init__(self, capacity):
        if not isinstance(capacity, int) or capacity < 1:
            raise ValueError("Capacity must be an integer >= 1")
        self._capacity = capacity
        self._tokens = capacity
        self._lock = threading.Lock()

    def allow(self, n=1):
        if not isinstance(n, int) or n < 1:
            raise ValueError("n must be an integer >= 1")
        
        with self._lock:
            if self._tokens >= n:
                self._tokens -= n
                return True
            return False

    def refill(self, n):
        if not isinstance(n, int) or n < 0:
            raise ValueError("n must be a non-negative integer")
        
        with self._lock:
            self._tokens = min(self._capacity, self._tokens + n)

    @property
    def tokens(self):
        with self._lock:
            return self._tokens
