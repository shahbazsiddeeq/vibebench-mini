import functools
import threading


def memoize(fn):
    """
    Decorator that caches results of `fn` keyed by its positional and
    keyword arguments (all must be hashable). Thread-safe: each distinct
    argument set is computed exactly once, even under concurrent access,
    and recursive calls (with different argument sets) do not deadlock.
    """
    cache = {}
    locks = {}
    global_lock = threading.Lock()

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))

        with global_lock:
            if key in cache:
                return cache[key]
            lock = locks.get(key)
            if lock is None:
                lock = threading.Lock()
                locks[key] = lock

        with lock:
            with global_lock:
                if key in cache:
                    return cache[key]

            result = fn(*args, **kwargs)

            with global_lock:
                cache[key] = result

            return result

    return wrapper
