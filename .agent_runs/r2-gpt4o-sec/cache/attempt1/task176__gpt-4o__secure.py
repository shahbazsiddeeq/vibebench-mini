import threading
import time
from collections import deque
from typing import Optional
import secrets

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
            if timeout is not None and timeout < 0:
                return False
            end_time = None if timeout is None else time.monotonic() + timeout
            while len(self.queue) >= self.capacity:
                if timeout == 0:
                    return False
                if timeout is not None:
                    remaining = end_time - time.monotonic()
                    if remaining <= 0 or not self.not_full.wait(remaining):
                        return False
                else:
                    self.not_full.wait()
            self.queue.append(item)
            self.not_empty.notify()
            return True

    def get(self, timeout: Optional[float] = None):
        with self.not_empty:
            if timeout is not None and timeout < 0:
                raise TimeoutError("Timeout must be non-negative")
            end_time = None if timeout is None else time.monotonic() + timeout
            while not self.queue:
                if timeout == 0:
                    raise TimeoutError("Queue is empty")
                if timeout is not None:
                    remaining = end_time - time.monotonic()
                    if remaining <= 0 or not self.not_empty.wait(remaining):
                        raise TimeoutError("Timeout expired")
                else:
                    self.not_empty.wait()
            item = self.queue.popleft()
            self.not_full.notify()
            return item

    def size(self) -> int:
        with self.lock:
            return len(self.queue)
