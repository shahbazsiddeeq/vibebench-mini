import threading
import contextlib

class ResourcePool:
    """
    A thread-safe class that limits how many threads may hold a resource at once.
    """

    def __init__(self, capacity: int):
        if capacity < 1:
            raise ValueError("Capacity must be at least 1.")
        self._capacity = capacity
        self._available_permits = capacity
        self._lock = threading.Lock()
        self._condition = threading.Condition(self._lock)

    def acquire(self, timeout: float | None = None) -> bool:
        """
        Blocks the calling thread while all capacity permits are checked out
        and returns True once a permit is granted, or returns False if timeout
        seconds elapse first.

        :param timeout: The maximum time to wait for a permit. None waits forever,
                        0 tries once without blocking.
        :return: True if a permit was acquired, False otherwise.
        """
        with self._condition:
            if self._available_permits > 0:
                self._available_permits -= 1
                return True
            elif timeout == 0:
                return False
            else:
                # Wait for a permit to become available
                # The predicate checks if a permit is available
                # wait() returns True if the predicate is true on return, False if timeout
                acquired = self._condition.wait_for(lambda: self._available_permits > 0, timeout=timeout)
                if acquired:
                    self._available_permits -= 1
                return acquired

    def release(self):
        """
        Returns one permit. Raises ValueError if called when no permits are
        currently checked out (i.e. it would push availability above capacity).
        """
        with self._condition:
            if self._available_permits >= self._capacity:
                raise ValueError("Cannot release: all permits are already available (over-release detected).")
            self._available_permits += 1
            self._condition.notify() # Notify one waiting thread

    def available(self) -> int:
        """
        Returns how many permits are currently free.
        """
        with self._lock:
            return self._available_permits

    @contextlib.contextmanager
    def slot(self, timeout: float | None = None):
        """
        Returns a context manager that acquires a permit on enter (raising
        TimeoutError if it cannot within timeout) and releases it on exit.
        """
        acquired = self.acquire(timeout=timeout)
        if not acquired:
            raise TimeoutError("Could not acquire a resource slot within the specified timeout.")
        try:
            yield
        finally:
            self.release()
