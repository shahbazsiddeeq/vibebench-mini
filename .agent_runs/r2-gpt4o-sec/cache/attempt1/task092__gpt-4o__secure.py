import functools
import threading

def memoize(fn):
    cache = {}
    lock = threading.Lock()

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        # Create a key based on the function's arguments
        key = (args, frozenset(kwargs.items()))
        
        # Use a lock to ensure thread safety
        with lock:
            if key not in cache:
                # Compute the result and store it in the cache
                cache[key] = fn(*args, **kwargs)
        
        return cache[key]

    return wrapper
