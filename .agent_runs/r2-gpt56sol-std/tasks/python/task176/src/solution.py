from collections import deque
import threading
import time
from typing import Any


class BoundedBlockingQueue:
    def __init__(self, capacity: int):
        if capacity < 1:
            raise ValueError("capacity must be at least 1")

        self._capacity = capacity
        self._items = deque()
        self._condition = threading.Condition()

    def put(self, item: Any, timeout: float | None = None) -> bool:
        with self._condition:
            if timeout is None:
                while len(self._items) >= self._capacity:
                    self._condition.wait()
            else:
                deadline = time.monotonic() + max(timeout, 0.0)
                while len(self._items) >= self._capacity:
                    remaining = deadline - time.monotonic()
                    if remaining <= 0:
                        return False
                    self._condition.wait(remaining)

            self._items.append(item)
            self._condition.notify_all()
            return True

    def get(self, timeout: float | None = None) -> Any:
        with self._condition:
            if timeout is None:
                while not self._items:
                    self._condition.wait()
            else:
                deadline = time.monotonic() + max(timeout, 0.0)
                while not self._items:
                    remaining = deadline - time.monotonic()
                    if remaining <= 0:
                        raise TimeoutError("timed out waiting for an item")
                    self._condition.wait(remaining)

            item = self._items.popleft()
            self._condition.notify_all()
            return item

    def size(self) -> int:
        with self._condition:
            return len(self._items)
