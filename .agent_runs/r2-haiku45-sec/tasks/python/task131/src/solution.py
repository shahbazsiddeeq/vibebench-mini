import threading
from typing import Any, Callable, Optional


class Once:
    """A thread-safe run-once initializer that caches the result of a callable."""
    
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._initialized = False
        self._cached_value: Any = None
    
    def do(self, fn: Callable[[], Any]) -> Any:
        """
        Run fn only the first time it succeeds, cache its return value,
        and return the cached value on subsequent calls.
        
        If fn raises an exception, it propagates to the caller and the run
        is NOT recorded, so a later do() call will attempt to run fn again.
        
        Args:
            fn: A zero-argument callable to run once.
            
        Returns:
            The cached return value from the first successful call to fn.
        """
        if not callable(fn):
            raise TypeError("fn must be callable")
        
        # Fast path: if already initialized, return cached value without lock
        if self._initialized:
            return self._cached_value
        
        # Slow path: acquire lock and check again (double-checked locking)
        with self._lock:
            # Check again in case another thread initialized while we waited
            if self._initialized:
                return self._cached_value
            
            # Run fn - if it raises, the exception propagates and we don't set _initialized
            result = fn()
            
            # Only mark as initialized after successful completion
            self._cached_value = result
            self._initialized = True
            
            return result
