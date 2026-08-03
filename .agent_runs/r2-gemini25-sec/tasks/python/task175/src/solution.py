import threading
import time

class CountDownLatch:
    """
    A synchronization aid that allows one or more threads to wait until a set of operations
    being performed in other threads completes.

    The latch is initialized with a count. The await_latch method blocks until the current
    count reaches zero due to invocations of the count_down() method, or until the
    specified waiting time elapses.

    A CountDownLatch is a one-shot phenomenon: once the count reaches zero, it cannot
    be reset. If you need a latch that resets, consider using a CyclicBarrier.
    """

    def __init__(self, count: int):
        """
        Initializes the latch with the given count.

        Args:
            count: The number of times count_down() must be invoked before threads can pass
                   through await_latch().

        Raises:
            ValueError: If count is negative.
        """
        if not isinstance(count, int):
            raise TypeError("count must be an integer")
        if count < 0:
            raise ValueError("count cannot be negative")

        self._count = count
        self._lock = threading.Lock()
        self._condition = threading.Condition(self._lock)

    def count_down(self) -> None:
        """
        Decrements the count of the latch.

        If the count reaches zero, all waiting threads are released.
        If the count is already zero, this method does nothing.
        """
        with self._lock:
            if self._count > 0:
                self._count -= 1
                if self._count == 0:
                    self._condition.notify_all()

    def await_latch(self, timeout: float | None = None) -> bool:
        """
        Causes the current thread to wait until the latch has counted down to zero,
        unless the thread is interrupted, or the specified waiting time elapses.

        Args:
            timeout: The maximum time to wait in seconds. If None, waits indefinitely.
                     If 0 or negative, checks the count immediately and returns.

        Returns:
            True if the count reached zero, False if the waiting time elapsed before
            the count reached zero.
        """
        if timeout is not None:
            if not isinstance(timeout, (int, float)):
                raise TypeError("timeout must be a float or None")
            if timeout < 0:
                # Treat negative timeout as 0 for practical purposes,
                # meaning non-blocking check.
                timeout = 0

        with self._lock:
            if self._count == 0:
                return True
            if timeout == 0:
                return False

            # Use _condition.wait() which handles spurious wakeups and reacquires the lock.
            # It returns True if the condition was met (notified), False if timeout.
            return self._condition.wait(timeout=timeout)

    def get_count(self) -> int:
        """
        Returns the current count.

        Returns:
            The current count.
        """
        with self._lock:
            return self._count
