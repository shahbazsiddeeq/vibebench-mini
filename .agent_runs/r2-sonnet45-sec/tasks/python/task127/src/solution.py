import threading


class TokenBucket:
    """Thread-safe token bucket rate limiter."""
    
    def __init__(self, capacity):
        """
        Initialize a token bucket with the given capacity.
        
        Args:
            capacity: Maximum number of tokens (must be >= 1)
            
        Raises:
            ValueError: If capacity < 1
        """
        if not isinstance(capacity, int) or capacity < 1:
            raise ValueError("Capacity must be an integer >= 1")
        
        self._capacity = capacity
        self._tokens = capacity
        self._lock = threading.Lock()
    
    def allow(self, n=1):
        """
        Attempt to consume n tokens atomically.
        
        Args:
            n: Number of tokens to consume (default: 1)
            
        Returns:
            True if n tokens were available and consumed, False otherwise.
            If False, no tokens are consumed (all-or-nothing).
        """
        if not isinstance(n, int) or n < 0:
            return False
        
        with self._lock:
            if self._tokens >= n:
                self._tokens -= n
                return True
            return False
    
    def refill(self, n):
        """
        Add n tokens to the bucket, capped at capacity.
        
        Args:
            n: Number of tokens to add
        """
        if not isinstance(n, int) or n < 0:
            return
        
        with self._lock:
            self._tokens = min(self._tokens + n, self._capacity)
    
    @property
    def tokens(self):
        """
        Get the current number of tokens in the bucket.
        
        Returns:
            Current token count
        """
        with self._lock:
            return self._tokens
