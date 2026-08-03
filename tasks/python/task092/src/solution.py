from __future__ import annotations

import threading
from functools import wraps
from typing import Callable


def memoize(fn: Callable) -> Callable:
    """Cache results of ``fn`` for hashable positional/keyword args.

    Thread-safe and recursion-safe: the wrapped function is executed OUTSIDE
    the shared cache lock (a short-lived per-key lock guards each computation),
    so recursive calls do not deadlock, and a given argument set is computed
    exactly once even under concurrent first calls.
    """
    cache: dict = {}
    key_locks: dict = {}
    guard = threading.Lock()

    @wraps(fn)
    def wrapper(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        # Fast path / obtain the per-key lock without holding it during fn().
        with guard:
            if key in cache:
                return cache[key]
            key_lock = key_locks.get(key)
            if key_lock is None:
                key_lock = threading.Lock()
                key_locks[key] = key_lock

        with key_lock:
            with guard:
                if key in cache:
                    return cache[key]
            # Computed outside the shared guard so recursion works and other
            # keys can be computed concurrently.
            result = fn(*args, **kwargs)
            with guard:
                cache[key] = result
                key_locks.pop(key, None)
            return result

    return wrapper
