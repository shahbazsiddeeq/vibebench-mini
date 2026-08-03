# src/solution.py

import threading

class TokenBucket:
    def __init__(self, capacity: int):
        if capacity < 1:
            raise ValueError("Capacity must be at least 1.")
        self._capacity = capacity
        self._tokens = capacity
        self._lock = threading.Lock()

    def allow(self, n: int = 1) -> bool:
        if n < 1:
            raise ValueError("Must consume at least one token.")
        
        with self._lock:
            if self._tokens >= n:
                self._tokens -= n
                return True
            return False

    def refill(self, n: int) -> None:
        if n < 0:
            raise ValueError("Cannot refill a negative number of tokens.")
        
        with self._lock:
            self._tokens = min(self._capacity, self._tokens + n)

    @property
    def tokens(self) -> int:
        with self._lock:
            return self._tokens
