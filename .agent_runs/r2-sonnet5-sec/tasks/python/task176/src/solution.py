"""
Thread-safe bounded blocking FIFO queue implementation.

This module provides a BoundedBlockingQueue class backed solely by the
Python standard library's threading primitives. It is designed to be
safe for concurrent use by multiple producer and consumer threads.
"""

import threading
from collections import deque
from typing import Any, Optional


class BoundedBlockingQueue:
    """
    A thread-safe FIFO queue with a fixed maximum capacity.

    Producers block on put() while the queue is full, and consumers
    block on get() while the queue is empty. Both operations support
    an optional timeout.
    """

    def __init__(self, capacity: int) -> None:
        if not isinstance(capacity, int) or isinstance(capacity, bool):
            raise ValueError("capacity must be an integer")
        if capacity < 1:
            raise ValueError("capacity must be >= 1")

        self._capacity = capacity
        self._items: deque = deque()
        self._lock = threading.Lock()
        self._not_full = threading.Condition(self._lock)
        self._not_empty = threading.Condition(self._lock)

    def put(self, item: Any, timeout: Optional[float] = None) -> bool:
        """
        Insert an item into the queue, blocking while the queue is full.

        Returns True once the item has been enqueued, or False if the
        given timeout (in seconds) elapses first without space becoming
        available. timeout=None waits forever; timeout=0 tries once
        without blocking.
        """
        if timeout is not None:
            if not isinstance(timeout, (int, float)) or isinstance(timeout, bool):
                raise TypeError("timeout must be a number or None")
            if timeout < 0:
                raise ValueError("timeout must be non-negative")

        with self._not_full:
            if len(self._items) >= self._capacity:
                if not self._not_full.wait_for(
                    lambda: len(self._items) < self._capacity, timeout=timeout
                ):
                    return False

            self._items.append(item)
            self._not_empty.notify()
            return True

    def get(self, timeout: Optional[float] = None) -> Any:
        """
        Remove and return the oldest item in the queue, blocking while
        the queue is empty.

        Raises TimeoutError if the given timeout (in seconds) elapses
        first without an item becoming available. timeout=None waits
        forever; timeout=0 tries once without blocking.
        """
        if timeout is not None:
            if not isinstance(timeout, (int, float)) or isinstance(timeout, bool):
                raise TypeError("timeout must be a number or None")
            if timeout < 0:
                raise ValueError("timeout must be non-negative")

        with self._not_empty:
            if not self._items:
                if not self._not_empty.wait_for(
                    lambda: len(self._items) > 0, timeout=timeout
                ):
                    raise TimeoutError("get() timed out waiting for an item")

            item = self._items.popleft()
            self._not_full.notify()
            return item

    def size(self) -> int:
        """Return the current number of buffered items."""
        with self._lock:
            return len(self._items)
