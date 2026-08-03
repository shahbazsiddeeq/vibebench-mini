import threading
from contextlib import contextmanager
from typing import Optional


class ResourcePool:
    """Thread-safe resource pool that limits concurrent access to a fixed capacity."""
    
    def __init__(self, capacity: int):
        """Initialize a resource pool with the given capacity.
        
        Args:
            capacity: Maximum number of concurrent permits (must be >= 1)
            
        Raises:
            ValueError: If capacity < 1
        """
        if not isinstance(capacity, int) or capacity < 1:
            raise ValueError("Capacity must be an integer >= 1")
        
        self._capacity = capacity
        self._semaphore = threading.Semaphore(capacity)
        self._lock = threading.Lock()
        self._acquired_count = 0
    
    def acquire(self, timeout: Optional[float] = None) -> bool:
        """Acquire a permit from the pool.
        
        Args:
            timeout: Maximum time to wait in seconds. None waits forever,
                    0 tries once without blocking.
                    
        Returns:
            True if a permit was acquired, False if timeout elapsed.
        """
        # Semaphore.acquire returns True on success, False on timeout
        acquired = self._semaphore.acquire(blocking=(timeout != 0), timeout=timeout)
        
        if acquired:
            with self._lock:
                self._acquired_count += 1
        
        return acquired
    
    def release(self) -> None:
        """Release a permit back to the pool.
        
        Raises:
            ValueError: If called when no permits are currently checked out
                       (would push availability above capacity).
        """
        with self._lock:
            if self._acquired_count <= 0:
                raise ValueError("Cannot release: no permits are currently acquired")
            self._acquired_count -= 1
        
        self._semaphore.release()
    
    def available(self) -> int:
        """Return the number of permits currently available.
        
        Returns:
            Number of free permits (0 to capacity).
        """
        with self._lock:
            return self._capacity - self._acquired_count
    
    @contextmanager
    def slot(self, timeout: Optional[float] = None):
        """Context manager that acquires a permit on enter and releases on exit.
        
        Args:
            timeout: Maximum time to wait for acquisition in seconds.
                    None waits forever.
                    
        Raises:
            TimeoutError: If unable to acquire within timeout.
            
        Yields:
            None
        """
        acquired = self.acquire(timeout=timeout)
        if not acquired:
            raise TimeoutError("Failed to acquire resource within timeout")
        
        try:
            yield
        finally:
            self.release()
