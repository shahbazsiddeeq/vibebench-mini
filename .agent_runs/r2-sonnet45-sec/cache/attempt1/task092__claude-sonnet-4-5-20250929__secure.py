import functools
import threading


def memoize(fn):
    """
    Decorator that caches function results based on arguments.
    Thread-safe and handles recursive calls without deadlocking.
    """
    cache = {}
    lock = threading.RLock()  # Reentrant lock to handle recursion
    
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        # Create a hashable cache key from positional and keyword arguments
        # Sort kwargs items to ensure consistent ordering
        try:
            if kwargs:
                # Convert kwargs to a sorted tuple of items for consistent hashing
                kwargs_tuple = tuple(sorted(kwargs.items()))
                cache_key = (args, kwargs_tuple)
            else:
                cache_key = (args, ())
        except TypeError:
            # If arguments are not hashable, we cannot cache
            # Fall back to calling the function directly
            return fn(*args, **kwargs)
        
        # Check cache first (with lock to ensure thread safety)
        with lock:
            if cache_key in cache:
                return cache[cache_key]
        
        # Compute result (lock is released during computation to allow recursion)
        # The RLock allows the same thread to re-acquire it during recursive calls
        result = fn(*args, **kwargs)
        
        # Store in cache
        with lock:
            # Double-check pattern: another thread might have computed it
            if cache_key not in cache:
                cache[cache_key] = result
        
        return result
    
    return wrapper
