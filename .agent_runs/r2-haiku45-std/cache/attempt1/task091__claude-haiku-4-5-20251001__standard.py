import threading


class AtomicCounter:
    """Thread-safe counter with atomic increment and decrement operations."""
    
    def __init__(self, initial=0):
        """Initialize the counter with an initial value.
        
        Args:
            initial: The initial value of the counter (default: 0)
            
        Raises:
            ValueError: If initial < 0
        """
        if initial < 0:
            raise ValueError("initial value cannot be negative")
        
        self._value = initial
        self._lock = threading.Lock()
    
    def increment(self) -> int:
        """Atomically increment the counter by 1 and return the new value.
        
        Returns:
            The new value after incrementing
        """
        with self._lock:
            self._value += 1
            return self._value
    
    def decrement(self) -> int:
        """Atomically decrement the counter by 1 and return the new value.
        
        Returns:
            The new value after decrementing
        """
        with self._lock:
            self._value -= 1
            return self._value
    
    def value(self) -> int:
        """Get the current value of the counter.
        
        Returns:
            The current value
        """
        with self._lock:
            return self._value
