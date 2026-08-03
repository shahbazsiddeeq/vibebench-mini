import threading
from contextlib import contextmanager
from typing import Optional


class ResourcePool:
    """Thread-safe resource pool that limits concurrent access using a semaphore."""
    
    def __init__(self, capacity: int) -> None:
        """Initialize the resource pool with a given capacity.
        
        Args:
            capacity: Maximum number of permits available. Must be >= 1.
            
        Raises:
            ValueError: If capacity < 1.
        """
        if capacity < 1:
            raise ValueError("capacity must be at least 1")
        
        self._capacity = capacity
        self._semaphore = threading.Semaphore(capacity)
        self._lock = threading.Lock()
        self._available = capacity
    
    def acquire(self, timeout: Optional[float] = None) -> bool:
        """Acquire a permit from the pool.
        
        Args:
            timeout: Maximum time to wait in seconds. None waits forever,
                    0 tries once without blocking.
        
        Returns:
            True if a permit was acquired, False if timeout elapsed.
        """
        acquired = self._semaphore.acquire(timeout=timeout)
        if acquired:
            with self._lock:
                self._available -= 1
        return acquired
    
    def release(self) -> None:
        """Release a permit back to the pool.
        
        Raises:
            ValueError: If no permits are currently checked out.
        """
        with self._lock:
            if self._available >= self._capacity:
                raise ValueError("cannot release more permits than capacity")
            self._available += 1
        self._semaphore.release()
    
    def available(self) -> int:
        """Return the number of permits currently available.
        
        Returns:
            Number of free permits.
        """
        with self._lock:
            return self._available
    
    @contextmanager
    def slot(self, timeout: Optional[float] = None):
        """Context manager that acquires and releases a permit.
        
        Args:
            timeout: Maximum time to wait for a permit in seconds.
                    None waits forever, 0 tries once without blocking.
        
        Yields:
            None
            
        Raises:
            TimeoutError: If a permit cannot be acquired within timeout.
        """
        acquired = self.acquire(timeout=timeout)
        if not acquired:
            raise TimeoutError("could not acquire permit within timeout")
        try:
            yield
        finally:
            self.release()
