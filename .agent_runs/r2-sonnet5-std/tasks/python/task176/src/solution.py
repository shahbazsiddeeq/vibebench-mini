"""Thread-safe bounded blocking FIFO queue implementation."""

import threading
from collections import deque


class BoundedBlockingQueue:
    def __init__(self, capacity: int):
        if capacity < 1:
            raise ValueError("capacity must be >= 1")
        self._capacity = capacity
        self._queue = deque()
        self._lock = threading.Lock()
        self._not_full = threading.Condition(self._lock)
        self._not_empty = threading.Condition(self._lock)

    def put(self, item, timeout: float | None = None) -> bool:
        with self._not_full:
            if timeout is None:
                while len(self._queue) >= self._capacity:
                    self._not_full.wait()
            elif timeout == 0:
                if len(self._queue) >= self._capacity:
                    return False
            else:
                deadline = None
                import time as _time
                deadline = _time.monotonic() + timeout
                while len(self._queue) >= self._capacity:
                    remaining = deadline - _time.monotonic()
                    if remaining <= 0:
                        return False
                    self._not_full.wait(remaining)

            self._queue.append(item)
            self._not_empty.notify()
            return True

    def get(self, timeout: float | None = None):
        with self._not_empty:
            if timeout is None:
                while len(self._queue) == 0:
                    self._not_empty.wait()
            elif timeout == 0:
                if len(self._queue) == 0:
                    raise TimeoutError("get timed out")
            else:
                import time as _time
                deadline = _time.monotonic() + timeout
                while len(self._queue) == 0:
                    remaining = deadline - _time.monotonic()
                    if remaining <= 0:
                        raise TimeoutError("get timed out")
                    self._not_empty.wait(remaining)

            item = self._queue.popleft()
            self._not_full.notify()
            return item

    def size(self) -> int:
        with self._lock:
            return len(self._queue)
