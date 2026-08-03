import threading
from collections import deque
from typing import Optional

class BoundedBlockingQueue:
    def __init__(self, capacity: int):
        if capacity < 1:
            raise ValueError("Capacity must be at least 1")
        self.capacity = capacity
        self.queue = deque()
        self.lock = threading.Lock()
        self.not_empty = threading.Condition(self.lock)
        self.not_full = threading.Condition(self.lock)

    def put(self, item, timeout: Optional[float] = None) -> bool:
        with self.not_full:
            if timeout is not None and timeout <= 0:
                if len(self.queue) >= self.capacity:
                    return False
            else:
                end_time = None if timeout is None else threading.current_thread().time() + timeout
                while len(self.queue) >= self.capacity:
                    remaining = None if end_time is None else end_time - threading.current_thread().time()
                    if remaining is not None and remaining <= 0:
                        return False
                    self.not_full.wait(remaining)
            self.queue.append(item)
            self.not_empty.notify()
            return True

    def get(self, timeout: Optional[float] = None):
        with self.not_empty:
            if timeout is not None and timeout <= 0:
                if not self.queue:
                    raise TimeoutError
            else:
                end_time = None if timeout is None else threading.current_thread().time() + timeout
                while not self.queue:
                    remaining = None if end_time is None else end_time - threading.current_thread().time()
                    if remaining is not None and remaining <= 0:
                        raise TimeoutError
                    self.not_empty.wait(remaining)
            item = self.queue.popleft()
            self.not_full.notify()
            return item

    def size(self) -> int:
        with self.lock:
            return len(self.queue)
