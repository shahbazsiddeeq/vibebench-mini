import threading
import time
from typing import Optional


class ResourcePool:
    """
    A thread-safe resource pool that limits how many threads may hold a resource at once.
    """

    def __init__(self, capacity: int):
        """
        Initializes the ResourcePool with a given capacity.

        Args:
            capacity: The maximum number of resources that can be held concurrently.

        Raises:
            ValueError: If capacity is less than 1.
        """
        if not isinstance(capacity, int) or capacity < 1:
            raise ValueError("Capacity must be a positive integer.")

        self._capacity = capacity
        self._available_permits = capacity
        self._lock = threading.Lock()
        self._condition = threading.Condition(self._lock)

    def acquire(self, timeout: Optional[float] = None) -> bool:
        """
        Acquires a permit from the pool.

        Blocks the calling thread while all capacity permits are checked out and
        returns True once a permit is granted, or returns False if timeout seconds
        elapse first.

        Args:
            timeout: The maximum time to wait for a permit in seconds.
                     None means wait indefinitely. 0 means try once without blocking.

        Returns:
            True if a permit was acquired, False otherwise.
        """
        if timeout is not None and not isinstance(timeout, (int, float)):
            raise ValueError("Timeout must be a number or None.")
        if isinstance(timeout, (int, float)) and timeout < 0:
            raise ValueError("Timeout cannot be negative.")

        with self._condition:
            if self._available_permits > 0:
                self._available_permits -= 1
                return True
            elif timeout == 0:
                return False
            else:
                # Wait for a permit to become available
                # The wait() method returns True if it was notified, False if timeout occurred.
                # We need to loop because of spurious wakeups and to re-check the condition.
                start_time = time.monotonic()
                while self._available_permits == 0:
                    if timeout is not None:
                        elapsed_time = time.monotonic() - start_time
                        remaining_timeout = timeout - elapsed_time
                        if remaining_timeout <= 0:
                            return False
                        if not self._condition.wait(remaining_timeout):
                            # Timeout occurred, and we still don't have a permit
                            return False
                    else:
                        self._condition.wait()
                
                # A permit is now available
                self._available_permits -= 1
                return True

    def release(self) -> None:
        """
        Releases a permit back to the pool.

        Raises:
            ValueError: If called when no permits are currently checked out
                        (i.e., it would push availability above capacity).
        """
        with self._condition:
            if self._available_permits >= self._capacity:
                raise ValueError("Cannot release: no permits are currently checked out.")
            self._available_permits += 1
            self._condition.notify()

    def available(self) -> int:
        """
        Returns the number of permits currently free.

        Returns:
            The number of available permits.
        """
        with self._lock:
            return self._available_permits

    def slot(self, timeout: Optional[float] = None):
        """
        Returns a context manager that acquires a permit on enter and releases it on exit.

        Args:
            timeout: The maximum time to wait for a permit in seconds.
                     None means wait indefinitely.

        Returns:
            A context manager.

        Raises:
            TimeoutError: If a permit cannot be acquired within the specified timeout.
        """
        if timeout is not None and not isinstance(timeout, (int, float)):
            raise ValueError("Timeout must be a number or None.")
        if isinstance(timeout, (int, float)) and timeout < 0:
            raise ValueError("Timeout cannot be negative.")

        return _ResourcePoolSlot(self, timeout)


class _ResourcePoolSlot:
    """
    Context manager for ResourcePool.
    """

    def __init__(self, pool: ResourcePool, timeout: Optional[float]):
        self._pool = pool
        self._timeout = timeout
        self._acquired = False

    def __enter__(self):
        if not self._pool.acquire(self._timeout):
            raise TimeoutError("Failed to acquire resource within the specified timeout.")
        self._acquired = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._acquired:
            self._pool.release()
            self._acquired = False
