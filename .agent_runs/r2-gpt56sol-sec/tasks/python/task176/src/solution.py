from collections import deque
import math
import numbers
import threading
import time
from typing import Any, Deque, Optional


class BoundedBlockingQueue:
    """A thread-safe, bounded FIFO queue."""

    def __init__(self, capacity: int):
        if isinstance(capacity, bool) or not isinstance(capacity, int):
            raise TypeError("capacity must be an integer")
        if capacity < 1:
            raise ValueError("capacity must be at least 1")

        self._capacity = capacity
        self._items: Deque[Any] = deque()
        self._condition = threading.Condition()

    @staticmethod
    def _validate_timeout(timeout: Optional[float]) -> Optional[float]:
        if timeout is None:
            return None
        if isinstance(timeout, bool) or not isinstance(timeout, numbers.Real):
            raise TypeError("timeout must be a real number or None")

        value = float(timeout)
        if math.isnan(value) or value < 0:
            raise ValueError("timeout must be non-negative")
        if math.isinf(value):
            return None
        return value

    def put(self, item: Any, timeout: Optional[float] = None) -> bool:
        timeout_value = self._validate_timeout(timeout)

        with self._condition:
            if timeout_value is None:
                while len(self._items) >= self._capacity:
                    self._condition.wait()
            else:
                deadline = time.monotonic() + timeout_value
                while len(self._items) >= self._capacity:
                    remaining = deadline - time.monotonic()
                    if remaining <= 0:
                        return False
                    self._condition.wait(remaining)

            self._items.append(item)
            self._condition.notify()
            return True

    def get(self, timeout: Optional[float] = None) -> Any:
        timeout_value = self._validate_timeout(timeout)

        with self._condition:
            if timeout_value is None:
                while not self._items:
                    self._condition.wait()
            else:
                deadline = time.monotonic() + timeout_value
                while not self._items:
                    remaining = deadline - time.monotonic()
                    if remaining <= 0:
                        raise TimeoutError("queue get timed out")
                    self._condition.wait(remaining)

            item = self._items.popleft()
            self._condition.notify()
            return item

    def size(self) -> int:
        with self._condition:
            return len(self._items)
