import threading
from contextlib import contextmanager
from typing import Optional


class ResourcePool:
    def __init__(self, capacity: int):
        if capacity < 1:
            raise ValueError("Capacity must be at least 1")
        
        self._capacity = capacity
        self._semaphore = threading.Semaphore(capacity)
        self._lock = threading.Lock()
        self._acquired_count = 0
    
    def acquire(self, timeout: Optional[float] = None) -> bool:
        """
        Acquire a permit from the pool.
        
        Args:
            timeout: Maximum time to wait in seconds. None means wait forever,
                    0 means try once without blocking.
        
        Returns:
            True if a permit was acquired, False if timeout elapsed.
        """
        acquired = self._semaphore.acquire(blocking=(timeout != 0), timeout=timeout if timeout != 0 else None)
        
        if acquired:
            with self._lock:
                self._acquired_count += 1
        
        return acquired
    
    def release(self):
        """
        Release a permit back to the pool.
        
        Raises:
            ValueError: If called when no permits are currently checked out.
        """
        with self._lock:
            if self._acquired_count == 0:
                raise ValueError("Cannot release: no permits are currently acquired")
            self._acquired_count -= 1
        
        self._semaphore.release()
    
    def available(self) -> int:
        """
        Return the number of permits currently available.
        """
        with self._lock:
            return self._capacity - self._acquired_count
    
    @contextmanager
    def slot(self, timeout: Optional[float] = None):
        """
        Context manager that acquires a permit on enter and releases on exit.
        
        Args:
            timeout: Maximum time to wait for acquisition. None means wait forever.
        
        Raises:
            TimeoutError: If a permit cannot be acquired within the timeout.
        """
        acquired = self.acquire(timeout=timeout)
        if not acquired:
            raise TimeoutError("Could not acquire resource within timeout")
        
        try:
            yield
        finally:
            self.release()
