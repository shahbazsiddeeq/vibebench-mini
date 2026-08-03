import threading
from typing import Optional


class CountDownLatch:
    """
    A thread-safe synchronization primitive that allows one or more threads
    to wait until a set of operations completes.
    """
    
    def __init__(self, count: int):
        """
        Initialize the latch with the given count.
        
        Args:
            count: The initial count value (must be >= 0)
            
        Raises:
            ValueError: If count is negative
        """
        if not isinstance(count, int):
            raise ValueError("count must be an integer")
        if count < 0:
            raise ValueError("count must be non-negative")
        
        self._count = count
        self._lock = threading.Lock()
        self._condition = threading.Condition(self._lock)
    
    def count_down(self) -> None:
        """
        Decrement the internal count by one, but never below zero.
        If the count reaches zero, all waiting threads are released.
        Calls when count is already 0 are no-ops.
        """
        with self._lock:
            if self._count > 0:
                self._count -= 1
                if self._count == 0:
                    # Notify all waiting threads
                    self._condition.notify_all()
    
    def await_latch(self, timeout: Optional[float] = None) -> bool:
        """
        Block the calling thread until the count reaches 0.
        
        Args:
            timeout: Maximum time to wait in seconds (None waits forever)
            
        Returns:
            True if the count reached 0, False if timeout elapsed
        """
        if timeout is not None:
            if not isinstance(timeout, (int, float)):
                raise ValueError("timeout must be a number or None")
            if timeout < 0:
                raise ValueError("timeout must be non-negative")
        
        with self._lock:
            # If already at zero, return immediately
            if self._count == 0:
                return True
            
            # Wait for the count to reach zero
            if timeout is None:
                # Wait indefinitely
                while self._count > 0:
                    self._condition.wait()
                return True
            else:
                # Wait with timeout
                return self._condition.wait_for(
                    lambda: self._count == 0,
                    timeout=timeout
                )
    
    def get_count(self) -> int:
        """
        Return the current count value.
        
        Returns:
            The current count
        """
        with self._lock:
            return self._count
