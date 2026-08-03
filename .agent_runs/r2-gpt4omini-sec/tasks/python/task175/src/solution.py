# src/solution.py

import threading
import time

class CountDownLatch:
    def __init__(self, count: int):
        if count < 0:
            raise ValueError("Count must be non-negative")
        self._count = count
        self._lock = threading.Lock()
        self._condition = threading.Condition(self._lock)
    
    def count_down(self):
        with self._lock:
            if self._count > 0:
                self._count -= 1
                if self._count == 0:
                    self._condition.notify_all()  # Release all waiting threads
    
    def await_latch(self, timeout: float = None) -> bool:
        with self._lock:
            if self._count == 0:
                return True  # Immediate return if count is already 0
            
            if timeout is not None:
                end_time = time.monotonic() + timeout
                remaining = timeout
                while self._count > 0 and remaining > 0:
                    remaining = end_time - time.monotonic()
                    self._condition.wait(remaining)
                return self._count == 0
            
            while self._count > 0:
                self._condition.wait()
            return True
    
    def get_count(self) -> int:
        with self._lock:
            return self._count
