# src/solution.py

import threading
import time

class BoundedBlockingQueue:
    def __init__(self, capacity: int):
        if capacity < 1:
            raise ValueError("Capacity must be at least 1.")
        self.capacity = capacity
        self.queue = []
        self.lock = threading.Lock()
        self.not_empty = threading.Condition(self.lock)
        self.not_full = threading.Condition(self.lock)

    def put(self, item, timeout: float = None) -> bool:
        if timeout is not None and timeout < 0:
            raise ValueError("Timeout must be non-negative.")
        
        with self.not_full:
            start_time = time.monotonic()
            while len(self.queue) >= self.capacity:
                if timeout is not None:
                    elapsed = time.monotonic() - start_time
                    if elapsed >= timeout:
                        return False
                self.not_full.wait(timeout)

            self.queue.append(item)
            self.not_empty.notify()
            return True

    def get(self, timeout: float = None):
        if timeout is not None and timeout < 0:
            raise ValueError("Timeout must be non-negative.")
        
        with self.not_empty:
            start_time = time.monotonic()
            while not self.queue:
                if timeout is not None:
                    elapsed = time.monotonic() - start_time
                    if elapsed >= timeout:
                        raise TimeoutError("Timeout while waiting for item.")
                self.not_empty.wait(timeout)

            item = self.queue.pop(0)
            self.not_full.notify()
            return item

    def size(self) -> int:
        with self.lock:
            return len(self.queue)
