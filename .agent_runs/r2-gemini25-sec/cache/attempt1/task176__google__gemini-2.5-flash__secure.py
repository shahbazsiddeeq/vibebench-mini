import collections
import threading
import time


class BoundedBlockingQueue:
    """
    A thread-safe FIFO queue with a bounded capacity.

    This queue blocks producers when full and consumers when empty,
    with optional timeouts for blocking operations.
    """

    def __init__(self, capacity: int):
        """
        Initializes a BoundedBlockingQueue with the given capacity.

        Args:
            capacity: The maximum number of items the queue can hold.

        Raises:
            ValueError: If capacity is less than 1.
        """
        if not isinstance(capacity, int) or capacity < 1:
            raise ValueError("Capacity must be a positive integer.")

        self._capacity = capacity
        self._queue = collections.deque()
        self._lock = threading.Lock()
        self._not_empty = threading.Condition(self._lock)  # Signaled when an item is added
        self._not_full = threading.Condition(self._lock)    # Signaled when an item is removed

    def put(self, item, timeout: float | None = None) -> bool:
        """
        Puts an item into the queue.

        If the queue is full, this method blocks until space becomes available
        or the specified timeout elapses.

        Args:
            item: The item to put into the queue.
            timeout: The maximum time (in seconds) to wait for space to become
                     available. If None, waits indefinitely. If 0, tries once
                     without blocking.

        Returns:
            True if the item was successfully enqueued, False if the timeout
            elapsed before space became available.
        """
        if not (timeout is None or (isinstance(timeout, (int, float)) and timeout >= 0)):
            raise ValueError("Timeout must be None or a non-negative number.")

        with self._lock:
            if self._queue_is_full():
                if timeout == 0:
                    return False
                # Wait for space to become available
                if not self._not_full.wait(timeout=timeout):
                    return False  # Timeout occurred

            # After waiting, check again if queue is full (another thread might have filled it)
            # This check is technically redundant if wait() returned True, but good for clarity
            # and robustness against spurious wakeups if not_full.wait() was used without a predicate.
            if self._queue_is_full():
                return False # Should not happen if wait() returned True, but defensive.

            self._queue.append(item)
            self._not_empty.notify()  # Signal that the queue is no longer empty
            return True

    def get(self, timeout: float | None = None):
        """
        Removes and returns the oldest item from the queue.

        If the queue is empty, this method blocks until an item becomes available
        or the specified timeout elapses.

        Args:
            timeout: The maximum time (in seconds) to wait for an item to become
                     available. If None, waits indefinitely. If 0, tries once
                     without blocking.

        Returns:
            The oldest item from the queue.

        Raises:
            TimeoutError: If the timeout elapsed before an item became available.
        """
        if not (timeout is None or (isinstance(timeout, (int, float)) and timeout >= 0)):
            raise ValueError("Timeout must be None or a non-negative number.")

        with self._lock:
            if self._queue_is_empty():
                if timeout == 0:
                    raise TimeoutError("Queue is empty and timeout is 0.")
                # Wait for an item to become available
                if not self._not_empty.wait(timeout=timeout):
                    raise TimeoutError("Timeout occurred while waiting for an item.")

            # After waiting, check again if queue is empty (another thread might have emptied it)
            if self._queue_is_empty():
                raise TimeoutError("Queue became empty after waiting (spurious wakeup or race).")

            item = self._queue.popleft()
            self._not_full.notify()  # Signal that the queue is no longer full
            return item

    def size(self) -> int:
        """
        Returns the current number of items in the queue.

        Returns:
            The number of items currently in the queue.
        """
        with self._lock:
            return len(self._queue)

    def _queue_is_full(self) -> bool:
        """Internal helper to check if the queue is full."""
        return len(self._queue) >= self._capacity

    def _queue_is_empty(self) -> bool:
        """Internal helper to check if the queue is empty."""
        return not self._queue
