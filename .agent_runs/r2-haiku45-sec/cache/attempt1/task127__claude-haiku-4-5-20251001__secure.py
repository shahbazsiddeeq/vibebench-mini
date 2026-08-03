import threading
from typing import Optional


class TokenBucket:
    """Thread-safe token bucket rate limiter."""
    
    def __init__(self, capacity: int) -> None:
        """
        Initialize a TokenBucket with the given capacity.
        
        Args:
            capacity: Maximum number of tokens. Must be >= 1.
            
        Raises:
            ValueError: If capacity < 1.
        """
        if not isinstance(capacity, int) or capacity < 1:
            raise ValueError("capacity must be an integer >= 1")
        
        self._capacity = capacity
        self._tokens = capacity
        self._lock = threading.Lock()
    
    def allow(self, n: int = 1) -> bool:
        """
        Atomically consume n tokens if available.
        
        Args:
            n: Number of tokens to consume. Defaults to 1.
            
        Returns:
            True if n tokens were consumed, False otherwise.
            If False, no tokens are consumed (all-or-nothing).
        """
        if not isinstance(n, int) or n < 0:
            raise ValueError("n must be a non-negative integer")
        
        with self._lock:
            if self._tokens >= n:
                self._tokens -= n
                return True
            return False
    
    def refill(self, n: int) -> None:
        """
        Add n tokens to the bucket, capped at capacity.
        
        Args:
            n: Number of tokens to add.
        """
        if not isinstance(n, int) or n < 0:
            raise ValueError("n must be a non-negative integer")
        
        with self._lock:
            self._tokens = min(self._tokens + n, self._capacity)
    
    @property
    def tokens(self) -> int:
        """
        Get the current number of tokens.
        
        Returns:
            Current token count.
        """
        with self._lock:
            return self._tokens
