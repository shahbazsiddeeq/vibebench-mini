import threading


class CountDownLatch:
    """A thread-safe countdown latch that allows threads to wait until a count reaches zero."""
    
    def __init__(self, count: int):
        """Initialize the latch with a given count.
        
        Args:
            count: The initial count. Must be >= 0.
            
        Raises:
            ValueError: If count < 0.
        """
        if count < 0:
            raise ValueError("count must be >= 0")
        
        self._count = count
        self._lock = threading.Lock()
        self._condition = threading.Condition(self._lock)
    
    def count_down(self) -> None:
        """Decrement the count by one, but never below zero.
        
        When the count reaches zero, all waiting threads are notified.
        """
        with self._condition:
            if self._count > 0:
                self._count -= 1
                if self._count == 0:
                    self._condition.notify_all()
    
    def await_latch(self, timeout: float | None = None) -> bool:
        """Wait until the count reaches zero or timeout elapses.
        
        Args:
            timeout: Maximum time to wait in seconds. None means wait forever.
            
        Returns:
            True if the count reached zero, False if timeout elapsed first.
        """
        with self._condition:
            # If already at zero, return immediately
            if self._count == 0:
                return True
            
            # Wait for the count to reach zero or timeout
            self._condition.wait(timeout=timeout)
            
            # Return True if count is now zero, False otherwise
            return self._count == 0
    
    def get_count(self) -> int:
        """Get the current count.
        
        Returns:
            The current count value.
        """
        with self._lock:
            return self._count
