"""Thread-safe memoization utilities."""

from __future__ import annotations

import functools
import threading
from typing import Any, Callable, Dict, Tuple


class _Pending:
    """Represents a computation currently in progress."""

    __slots__ = ("owner", "event", "succeeded", "value", "error")

    def __init__(self, owner: int) -> None:
        self.owner = owner
        self.event = threading.Event()
        self.succeeded = False
        self.value: Any = None
        self.error: BaseException | None = None


def memoize(fn: Callable[..., Any]) -> Callable[..., Any]:
    """Cache results by positional and keyword arguments.

    Only successful results are cached. Concurrent calls with the same
    arguments share one computation. Recursive calls with different arguments
    remain safe because the lock is not held while the function executes.
    """
    if not callable(fn):
        raise TypeError("memoize requires a callable")

    cache: Dict[Tuple[Any, ...], Any] = {}
    pending: Dict[Tuple[Any, ...], _Pending] = {}
    lock = threading.RLock()

    @functools.wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # Keyword names are strings, so sorting is deterministic. Constructing
        # and using this key also validates that all argument values are
        # hashable.
        key = (args, tuple(sorted(kwargs.items())))
        hash(key)

        thread_id = threading.get_ident()

        with lock:
            if key in cache:
                return cache[key]

            current = pending.get(key)
            if current is None:
                current = _Pending(thread_id)
                pending[key] = current
                is_owner = True
            elif current.owner == thread_id:
                # Avoid deadlocking on a reentrant call with the exact same key.
                # Such a call cannot consume an unfinished cached result.
                is_owner = False
                reentrant = True
            else:
                is_owner = False
                reentrant = False

        if not is_owner:
            if reentrant:
                return fn(*args, **kwargs)

            current.event.wait()
            if current.succeeded:
                return current.value
            if current.error is not None:
                raise current.error
            raise RuntimeError("memoized computation did not complete")

        try:
            result = fn(*args, **kwargs)
        except BaseException as exc:
            with lock:
                if pending.get(key) is current:
                    del pending[key]
                current.error = exc
                current.event.set()
            raise

        with lock:
            cache[key] = result
            if pending.get(key) is current:
                del pending[key]
            current.value = result
            current.succeeded = True
            current.event.set()

        return result

    return wrapper
