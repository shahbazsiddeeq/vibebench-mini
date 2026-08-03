import threading
from collections import deque
from typing import Any, Optional


class BoundedBlockingQueue:
    """Thread-safe FIFO queue with bounded capacity."""
    
    def __init__(self, capacity: int) -> None:
        """Initialize the queue with a given capacity.
        
        Args:
            capacity: Maximum number of items the queue can hold.
            
        Raises:
            ValueError: If capacity < 1.
        """
        if capacity < 1:
            raise ValueError("capacity must be at least 1")
        
        self._capacity = capacity
        self._queue: deque = deque()
        self._lock = threading.RLock()
        self._not_full = threading.Condition(self._lock)
        self._not_empty = threading.Condition(self._lock)
    
    def put(self, item: Any, timeout: Optional[float] = None) -> bool:
        """Put an item into the queue.
        
        Blocks while the queue is at capacity. Returns True once the item
        is enqueued, or False if timeout seconds elapse without space becoming
        available.
        
        Args:
            item: The item to enqueue.
            timeout: Maximum seconds to wait. None waits forever, 0 tries once.
            
        Returns:
            True if item was enqueued, False if timeout elapsed.
        """
        with self._not_full:
            # Handle timeout=0 case: try once without blocking
            if timeout == 0:
                if len(self._queue) >= self._capacity:
                    return False
            else:
                # Wait until there's space, with optional timeout
                while len(self._queue) >= self._capacity:
                    if not self._not_full.wait(timeout=timeout):
                        return False
            
            # Enqueue the item
            self._queue.append(item)
            # Notify any waiting consumers
            self._not_empty.notify()
            return True
    
    def get(self, timeout: Optional[float] = None) -> Any:
        """Get and remove the oldest item from the queue.
        
        Blocks while the queue is empty.
        
        Args:
            timeout: Maximum seconds to wait. None waits forever.
            
        Returns:
            The oldest item in the queue.
            
        Raises:
            TimeoutError: If timeout seconds elapse without an item becoming available.
        """
        with self._not_empty:
            # Wait until there's an item, with optional timeout
            while len(self._queue) == 0:
                if not self._not_empty.wait(timeout=timeout):
                    raise TimeoutError("Queue is empty and timeout elapsed")
            
            # Dequeue the item
            item = self._queue.popleft()
            # Notify any waiting producers
            self._not_full.notify()
            return item
    
    def size(self) -> int:
        """Return the current number of items in the queue.
        
        Returns:
            The number of items currently buffered.
        """
        with self._lock:
            return len(self._queue)
