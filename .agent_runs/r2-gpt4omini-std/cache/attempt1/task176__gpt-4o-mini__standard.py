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
        with self.not_full:
            if timeout is None:
                while len(self.queue) >= self.capacity:
                    self.not_full.wait()
            else:
                end_time = time.monotonic() + timeout
                while len(self.queue) >= self.capacity:
                    remaining = end_time - time.monotonic()
                    if remaining <= 0:
                        return False
                    self.not_full.wait(remaining)

            self.queue.append(item)
            self.not_empty.notify()
            return True

    def get(self, timeout: float = None):
        with self.not_empty:
            if timeout is None:
                while not self.queue:
                    self.not_empty.wait()
            else:
                end_time = time.monotonic() + timeout
                while not self.queue:
                    remaining = end_time - time.monotonic()
                    if remaining <= 0:
                        raise TimeoutError("Timeout while waiting for item.")
                    self.not_empty.wait(remaining)

            item = self.queue.pop(0)
            self.not_full.notify()
            return item

    def size(self) -> int:
        with self.lock:
            return len(self.queue)
