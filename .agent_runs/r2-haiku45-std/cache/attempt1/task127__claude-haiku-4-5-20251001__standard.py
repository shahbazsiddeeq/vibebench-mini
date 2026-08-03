import threading


class TokenBucket:
    """Thread-safe token bucket rate limiter."""
    
    def __init__(self, capacity):
        """Initialize TokenBucket with given capacity.
        
        Args:
            capacity: Maximum number of tokens (must be >= 1)
            
        Raises:
            ValueError: If capacity < 1
        """
        if capacity < 1:
            raise ValueError("capacity must be >= 1")
        
        self._capacity = capacity
        self._tokens = capacity
        self._lock = threading.Lock()
    
    def allow(self, n=1):
        """Atomically consume n tokens if available.
        
        Args:
            n: Number of tokens to consume (default 1)
            
        Returns:
            True if n tokens were consumed, False otherwise (all-or-nothing)
        """
        with self._lock:
            if self._tokens >= n:
                self._tokens -= n
                return True
            return False
    
    def refill(self, n):
        """Add n tokens, capped at capacity.
        
        Args:
            n: Number of tokens to add
        """
        with self._lock:
            self._tokens = min(self._tokens + n, self._capacity)
    
    @property
    def tokens(self):
        """Get current token count (read-only).
        
        Returns:
            Current number of tokens
        """
        with self._lock:
            return self._tokens
