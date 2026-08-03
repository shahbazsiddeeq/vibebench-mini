import threading


class Once:
    """A run-once initializer that executes a callable only once and caches the result."""
    
    def __init__(self):
        self._lock = threading.Lock()
        self._initialized = False
        self._cached_value = None
    
    def do(self, fn):
        """
        Run fn only the first time it succeeds, cache its return value,
        and return the cached value on subsequent calls.
        
        If fn raises an exception, it propagates to the caller and the run
        is NOT recorded, so a later do(...) call will attempt to run fn again.
        
        Args:
            fn: A zero-arg callable to run
            
        Returns:
            The cached return value from the first successful execution of fn
        """
        if self._initialized:
            return self._cached_value
        
        with self._lock:
            # Double-check pattern: check again after acquiring lock
            if self._initialized:
                return self._cached_value
            
            # Run fn - if it raises, the exception propagates and we don't mark as initialized
            result = fn()
            
            # Only mark as initialized if fn() succeeded
            self._cached_value = result
            self._initialized = True
            
            return result
