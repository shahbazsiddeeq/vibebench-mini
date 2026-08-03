import collections
import threading


class BoundedBlockingQueue:
    """A thread-safe FIFO queue that blocks on a full put and an empty get."""

    def __init__(self, capacity):
        if capacity < 1:
            raise ValueError("capacity must be at least 1")
        self._capacity = capacity
        self._items = collections.deque()
        self._cond = threading.Condition()

    def put(self, item, timeout=None):
        with self._cond:
            if not self._cond.wait_for(
                lambda: len(self._items) < self._capacity, timeout
            ):
                return False
            self._items.append(item)
            self._cond.notify_all()
            return True

    def get(self, timeout=None):
        with self._cond:
            if not self._cond.wait_for(lambda: len(self._items) > 0, timeout):
                raise TimeoutError("get timed out while queue was empty")
            item = self._items.popleft()
            self._cond.notify_all()
            return item

    def size(self):
        with self._cond:
            return len(self._items)
