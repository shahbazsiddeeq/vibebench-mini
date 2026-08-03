import threading
from collections import deque
from typing import Any, Optional


class BoundedBlockingQueue:
    def __init__(self, capacity: int):
        if capacity < 1:
            raise ValueError("capacity must be at least 1")
        self.capacity = capacity
        self.queue = deque()
        self.lock = threading.Lock()
        self.not_full = threading.Condition(self.lock)
        self.not_empty = threading.Condition(self.lock)
    
    def put(self, item: Any, timeout: Optional[float] = None) -> bool:
        """
        Put an item into the queue.
        Blocks while the queue is full.
        Returns True if item was enqueued, False if timeout elapsed.
        """
        with self.not_full:
            # Wait until there's space in the queue
            if not self.not_full.wait_for(
                lambda: len(self.queue) < self.capacity,
                timeout=timeout
            ):
                # Timeout elapsed without space becoming available
                return False
            
            # Add item to queue
            self.queue.append(item)
            # Notify any waiting consumers
            self.not_empty.notify()
            return True
    
    def get(self, timeout: Optional[float] = None) -> Any:
        """
        Get and remove the oldest item from the queue.
        Blocks while the queue is empty.
        Raises TimeoutError if timeout seconds elapse without an item available.
        """
        with self.not_empty:
            # Wait until there's an item in the queue
            if not self.not_empty.wait_for(
                lambda: len(self.queue) > 0,
                timeout=timeout
            ):
                # Timeout elapsed without item becoming available
                raise TimeoutError()
            
            # Remove and return the oldest item
            item = self.queue.popleft()
            # Notify any waiting producers
            self.not_full.notify()
            return item
    
    def size(self) -> int:
        """Return the current number of items in the queue."""
        with self.lock:
            return len(self.queue)
