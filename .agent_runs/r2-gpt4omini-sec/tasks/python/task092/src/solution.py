import threading
from functools import wraps

def memoize(fn):
    cache = {}
    lock = threading.Lock()

    @wraps(fn)
    def wrapper(*args, **kwargs):
        # Create a key from the arguments
        key = (args, frozenset(kwargs.items()))
        
        with lock:
            if key not in cache:
                # Call the function and store the result in the cache
                cache[key] = fn(*args, **kwargs)
        
        return cache[key]

    return wrapper
