import threading
from typing import Optional


class CountDownLatch:
    """Thread-safe count-down latch for synchronizing threads."""
    
    def __init__(self, count: int) -> None:
        """
        Initialize a CountDownLatch with the given count.
        
        Args:
            count: Initial count value
            
        Raises:
            ValueError: If count < 0
        """
        if not isinstance(count, int) or count < 0:
            raise ValueError("count must be a non-negative integer")
        
        self._count = count
        self._lock = threading.Lock()
        self._condition = threading.Condition(self._lock)
    
    def count_down(self) -> None:
        """
        Decrement the count by one, but never below zero.
        
        If the count reaches zero, all waiting threads are notified.
        """
        with self._condition:
            if self._count > 0:
                self._count -= 1
                if self._count == 0:
                    self._condition.notify_all()
    
    def await_latch(self, timeout: Optional[float] = None) -> bool:
        """
        Block until the count reaches zero or timeout elapses.
        
        Args:
            timeout: Maximum time to wait in seconds, or None to wait forever
            
        Returns:
            True if count reached zero, False if timeout elapsed first
        """
        with self._condition:
            # If already at zero, return immediately
            if self._count == 0:
                return True
            
            # Wait for count to reach zero or timeout
            # wait() returns True if notified, False if timeout
            return self._condition.wait(timeout=timeout)
    
    def get_count(self) -> int:
        """
        Get the current count value.
        
        Returns:
            Current count
        """
        with self._lock:
            return self._count
