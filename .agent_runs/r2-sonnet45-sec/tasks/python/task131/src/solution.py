import threading


class Once:
    """
    A thread-safe run-once initializer that executes a callable exactly once
    on first successful completion and caches its return value.
    """
    
    def __init__(self):
        self._lock = threading.Lock()
        self._initialized = False
        self._value = None
    
    def do(self, fn):
        """
        Execute fn only on the first successful call, cache and return its result.
        
        Args:
            fn: A zero-argument callable to execute once
            
        Returns:
            The cached return value from the first successful execution of fn
            
        Raises:
            Any exception raised by fn (and does not mark as initialized)
        """
        # Fast path: if already initialized, return cached value without locking
        if self._initialized:
            return self._value
        
        # Slow path: acquire lock and check again (double-checked locking)
        with self._lock:
            # Check again in case another thread initialized while we waited
            if self._initialized:
                return self._value
            
            # Execute the callable - if it raises, we don't mark as initialized
            result = fn()
            
            # Only mark as initialized after successful execution
            self._value = result
            self._initialized = True
            
            return result
