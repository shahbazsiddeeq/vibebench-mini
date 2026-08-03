import functools
import threading

def memoize(fn):
    cache = {}
    lock = threading.Lock()

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        key = (args, frozenset(kwargs.items()))
        with lock:
            if key not in cache:
                cache[key] = fn(*args, **kwargs)
        return cache[key]

    return wrapper
