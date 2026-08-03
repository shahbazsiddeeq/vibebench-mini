import functools
import threading


def memoize(fn):
    """
    Decorator that caches function results based on arguments.
    Thread-safe and handles recursive calls without deadlocking.
    """
    cache = {}
    lock = threading.RLock()  # Reentrant lock to avoid deadlock on recursion
    
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        # Create a hashable key from positional and keyword arguments
        # Convert kwargs to a sorted tuple of items for consistent hashing
        key = (args, tuple(sorted(kwargs.items())))
        
        # Check if result is already cached
        with lock:
            if key in cache:
                return cache[key]
        
        # Compute the result (lock is released during computation for recursion)
        # But we need to ensure only one thread computes for a given key
        # Use double-checked locking pattern
        with lock:
            # Check again in case another thread computed it while we waited
            if key in cache:
                return cache[key]
            
            # Compute and cache the result
            # The RLock allows the same thread to re-enter during recursive calls
            result = fn(*args, **kwargs)
            cache[key] = result
            return result
    
    return wrapper
