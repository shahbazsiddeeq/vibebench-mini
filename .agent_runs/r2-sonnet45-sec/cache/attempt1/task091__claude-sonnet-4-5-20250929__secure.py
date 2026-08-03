import threading


class AtomicCounter:
    """Thread-safe counter with atomic increment, decrement, and value operations."""
    
    def __init__(self, initial=0):
        """
        Initialize the counter with an initial value.
        
        Args:
            initial: The initial counter value (must be >= 0)
            
        Raises:
            ValueError: If initial value is negative
        """
        if not isinstance(initial, int):
            raise ValueError("Initial value must be an integer")
        if initial < 0:
            raise ValueError("Initial value must be non-negative")
        
        self._value = initial
        self._lock = threading.Lock()
    
    def increment(self):
        """
        Atomically increment the counter by 1.
        
        Returns:
            The new counter value after incrementing
        """
        with self._lock:
            self._value += 1
            return self._value
    
    def decrement(self):
        """
        Atomically decrement the counter by 1.
        
        Returns:
            The new counter value after decrementing
        """
        with self._lock:
            self._value -= 1
            return self._value
    
    def value(self):
        """
        Get the current counter value atomically.
        
        Returns:
            The current counter value
        """
        with self._lock:
            return self._value
