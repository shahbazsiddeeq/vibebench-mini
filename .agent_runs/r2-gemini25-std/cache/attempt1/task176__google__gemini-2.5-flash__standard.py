import collections
import threading
import time


class BoundedBlockingQueue:
    def __init__(self, capacity: int):
        if capacity < 1:
            raise ValueError("Capacity must be at least 1")
        self._capacity = capacity
        self._queue = collections.deque()
        self._lock = threading.Lock()
        self._not_full = threading.Condition(self._lock)
        self._not_empty = threading.Condition(self._lock)

    def put(self, item, timeout: float | None = None) -> bool:
        with self._not_full:
            if timeout is not None and timeout < 0:
                timeout = 0  # Treat negative timeout as non-blocking

            if self._not_full.wait_for(lambda: len(self._queue) < self._capacity, timeout=timeout):
                self._queue.append(item)
                self._not_empty.notify()
                return True
            else:
                return False

    def get(self, timeout: float | None = None):
        with self._not_empty:
            if timeout is not None and timeout < 0:
                timeout = 0  # Treat negative timeout as non-blocking

            if self._not_empty.wait_for(lambda: len(self._queue) > 0, timeout=timeout):
                item = self._queue.popleft()
                self._not_full.notify()
                return item
            else:
                raise TimeoutError("Timeout elapsed while waiting for item")

    def size(self) -> int:
        with self._lock:
            return len(self._queue)
