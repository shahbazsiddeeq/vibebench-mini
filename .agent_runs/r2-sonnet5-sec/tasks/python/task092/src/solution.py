"""
A thread-safe memoization decorator.

Provides `memoize(fn)`, which wraps a callable so that results are cached
based on the (hashable) positional and keyword arguments used to call it.
The implementation is safe under concurrent access from multiple threads
and does not deadlock even when the wrapped function is recursive.
"""

import functools
import threading
from typing import Any, Callable, Dict, Tuple


def memoize(fn: Callable[..., Any]) -> Callable[..., Any]:
    """
    Return a memoizing wrapper around `fn`.

    - Results are cached by a key derived from the call's positional and
      keyword arguments. All arguments must be hashable; otherwise a
      TypeError is raised (arguments are not otherwise inspected or
      exposed in error messages to avoid leaking internal details).
    - The wrapper is safe for concurrent use from multiple threads: each
      distinct argument set is computed at most once, and concurrent calls
      with the same arguments will not race.
    - Recursive calls to the memoized function (even with the same
      arguments, from the same thread) will not deadlock, thanks to the
      use of per-key reentrant locks.
    - functools.wraps is used to preserve the wrapped function's metadata.
    """
    if not callable(fn):
        raise TypeError("memoize requires a callable")

    cache: Dict[Any, Any] = {}
    locks: Dict[Any, threading.RLock] = {}
    # Guards access to the `locks` and `cache` dictionaries themselves.
    registry_lock = threading.Lock()

    def _make_key(args: Tuple[Any, ...], kwargs: Dict[str, Any]) -> Any:
        try:
            # Sort kwargs by key name for a stable, order-independent key.
            sorted_kwargs = tuple(sorted(kwargs.items()))
            key = (args, sorted_kwargs)
            # Ensure the key itself is hashable (raises TypeError if not).
            hash(key)
            return key
        except TypeError:
            # Do not leak the actual (potentially sensitive) argument
            # values in the error message.
            raise TypeError(
                "memoize: all positional and keyword arguments must be hashable"
            ) from None

    @functools.wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        key = _make_key(args, kwargs)

        with registry_lock:
            lock = locks.get(key)
            if lock is None:
                lock = threading.RLock()
                locks[key] = lock

        with lock:
            if key in cache:
                return cache[key]
            result = fn(*args, **kwargs)
            cache[key] = result
            return result

    return wrapper
