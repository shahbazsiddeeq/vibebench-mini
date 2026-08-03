import threading
import time
from collections import deque


class BoundedBlockingQueue:
    def __init__(self, capacity: int):
        if capacity < 1:
            raise ValueError("Capacity must be at least 1")
        self.capacity = capacity
        self.queue = deque()
        self.lock = threading.Lock()
        self.not_full = threading.Condition(self.lock)
        self.not_empty = threading.Condition(self.lock)
    
    def put(self, item, timeout: float | None = None) -> bool:
        """
        Add an item to the queue. Blocks if the queue is full.
        
        Args:
            item: The item to add
            timeout: Maximum time to wait in seconds (None = wait forever, 0 = don't wait)
        
        Returns:
            True if item was added, False if timeout occurred
        """
        with self.not_full:
            if timeout is None:
                # Wait forever
                while len(self.queue) >= self.capacity:
                    self.not_full.wait()
                self.queue.append(item)
                self.not_empty.notify()
                return True
            elif timeout == 0:
                # Try once without blocking
                if len(self.queue) >= self.capacity:
                    return False
                self.queue.append(item)
                self.not_empty.notify()
                return True
            else:
                # Wait with timeout
                end_time = time.monotonic() + timeout
                while len(self.queue) >= self.capacity:
                    remaining = end_time - time.monotonic()
                    if remaining <= 0:
                        return False
                    self.not_full.wait(timeout=remaining)
                    if len(self.queue) < self.capacity:
                        break
                
                # Check again after wait
                if len(self.queue) >= self.capacity:
                    return False
                
                self.queue.append(item)
                self.not_empty.notify()
                return True
    
    def get(self, timeout: float | None = None):
        """
        Remove and return the oldest item from the queue. Blocks if the queue is empty.
        
        Args:
            timeout: Maximum time to wait in seconds (None = wait forever)
        
        Returns:
            The oldest item in the queue
        
        Raises:
            TimeoutError: If timeout occurs before an item is available
        """
        with self.not_empty:
            if timeout is None:
                # Wait forever
                while len(self.queue) == 0:
                    self.not_empty.wait()
                item = self.queue.popleft()
                self.not_full.notify()
                return item
            else:
                # Wait with timeout
                end_time = time.monotonic() + timeout
                while len(self.queue) == 0:
                    remaining = end_time - time.monotonic()
                    if remaining <= 0:
                        raise TimeoutError()
                    self.not_empty.wait(timeout=remaining)
                    if len(self.queue) > 0:
                        break
                
                # Check again after wait
                if len(self.queue) == 0:
                    raise TimeoutError()
                
                item = self.queue.popleft()
                self.not_full.notify()
                return item
    
    def size(self) -> int:
        """
        Return the current number of items in the queue.
        
        Returns:
            The number of items currently in the queue
        """
        with self.lock:
            return len(self.queue)
