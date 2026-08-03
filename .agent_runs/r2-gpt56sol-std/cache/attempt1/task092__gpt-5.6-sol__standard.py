"""Thread-safe memoization utilities."""

from functools import wraps
import threading


_MISSING = object()


class _Pending:
    __slots__ = ("owner", "event", "exception")

    def __init__(self, owner):
        self.owner = owner
        self.event = threading.Event()
        self.exception = _MISSING


def memoize(fn):
    """Cache results by positional and keyword arguments.

    Calls using the same arguments share one computation, including when made
    concurrently by multiple threads. Exceptions are not cached.
    """
    cache = {}
    pending = {}
    lock = threading.RLock()

    @wraps(fn)
    def wrapper(*args, **kwargs):
        key = (args, frozenset(kwargs.items()))
        current_thread = threading.current_thread()

        with lock:
            result = cache.get(key, _MISSING)
            if result is not _MISSING:
                return result

            flight = pending.get(key)
            if flight is None:
                flight = _Pending(current_thread)
                pending[key] = flight
                compute = True
            elif flight.owner is current_thread:
                # Recursive re-entry for the exact same key cannot wait for
                # itself. Ordinary recursion with different keys still uses
                # the cache normally.
                compute = False
                recursive_reentry = True
            else:
                compute = False
                recursive_reentry = False

        if not compute:
            if recursive_reentry:
                return fn(*args, **kwargs)

            flight.event.wait()
            if flight.exception is not _MISSING:
                raise flight.exception

            with lock:
                return cache[key]

        try:
            result = fn(*args, **kwargs)
        except BaseException as exc:
            with lock:
                if pending.get(key) is flight:
                    del pending[key]
                flight.exception = exc
                flight.event.set()
            raise

        with lock:
            cache[key] = result
            if pending.get(key) is flight:
                del pending[key]
            flight.event.set()

        return result

    return wrapper
