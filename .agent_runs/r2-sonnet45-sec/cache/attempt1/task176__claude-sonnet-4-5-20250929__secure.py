import threading
from collections import deque
from typing import Any


class BoundedBlockingQueue:
    """Thread-safe FIFO bounded blocking queue implementation."""
    
    def __init__(self, capacity: int):
        """Initialize a bounded blocking queue with the given capacity.
        
        Args:
            capacity: Maximum number of items the queue can hold.
            
        Raises:
            ValueError: If capacity < 1.
        """
        if not isinstance(capacity, int) or capacity < 1:
            raise ValueError("Capacity must be an integer >= 1")
        
        self._capacity = capacity
        self._queue = deque()
        self._lock = threading.Lock()
        self._not_full = threading.Condition(self._lock)
        self._not_empty = threading.Condition(self._lock)
    
    def put(self, item: Any, timeout: float | None = None) -> bool:
        """Add an item to the queue, blocking if full.
        
        Args:
            item: The item to add to the queue.
            timeout: Maximum time to wait in seconds. None waits forever,
                    0 tries once without blocking.
                    
        Returns:
            True if the item was successfully added, False if timeout elapsed.
        """
        with self._not_full:
            # Check if queue is full
            if len(self._queue) >= self._capacity:
                if timeout == 0:
                    return False
                
                # Wait for space to become available
                if not self._not_full.wait(timeout=timeout):
                    # Timeout occurred
                    return False
                
                # After waking up, check again if there's space
                if len(self._queue) >= self._capacity:
                    return False
            
            # Add item to queue
            self._queue.append(item)
            
            # Notify waiting consumers
            self._not_empty.notify()
            
            return True
    
    def get(self, timeout: float | None = None) -> Any:
        """Remove and return the oldest item from the queue, blocking if empty.
        
        Args:
            timeout: Maximum time to wait in seconds. None waits forever.
                    
        Returns:
            The oldest item in the queue.
            
        Raises:
            TimeoutError: If timeout elapsed before an item became available.
        """
        with self._not_empty:
            # Check if queue is empty
            if len(self._queue) == 0:
                # Wait for an item to become available
                if not self._not_empty.wait(timeout=timeout):
                    # Timeout occurred
                    raise TimeoutError("Queue is empty and timeout elapsed")
                
                # After waking up, check again if there's an item
                if len(self._queue) == 0:
                    raise TimeoutError("Queue is empty and timeout elapsed")
            
            # Remove and return the oldest item
            item = self._queue.popleft()
            
            # Notify waiting producers
            self._not_full.notify()
            
            return item
    
    def size(self) -> int:
        """Return the current number of items in the queue.
        
        Returns:
            The number of items currently in the queue.
        """
        with self._lock:
            return len(self._queue)
