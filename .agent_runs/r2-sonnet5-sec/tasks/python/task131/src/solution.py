"""
src/solution.py

Run-Once Initializer.

Provides a `Once` class whose `do(fn)` method executes the zero-argument
callable `fn` only the first time it *successfully* completes (across all
threads), caching and returning its result on every subsequent call.

If `fn` raises an exception, the exception propagates to the caller and the
attempt is not recorded as successful -- a later call to `do(...)` will try
to run `fn` (or a different callable) again.

Thread-safety:
    A double-checked locking pattern with a `threading.Lock` guarantees that
    only one thread ever executes the callable to completion, and that all
    threads observe a consistent, correctly cached result afterward.

Security considerations:
    - No use of eval/exec or dynamic code execution.
    - No external/untrusted data is parsed here; the module only manages
      call-once semantics for a callable supplied by the caller.
    - Errors from the callable are not swallowed or altered; they propagate
      unchanged but no internal state is exposed accidentally beyond what
      the callable itself provides.
"""

import threading
from typing import Any, Callable


class Once:
    """A run-once initializer.

    Usage:
        o = Once()
        o.do(fn)  # runs fn only once (on first success), caches result
    """

    __slots__ = ("_lock", "_done", "_value")

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._done = False
        self._value: Any = None

    def do(self, fn: Callable[[], Any]) -> Any:
        """Run `fn` exactly once (on first success) and cache its result.

        Args:
            fn: A zero-argument callable to invoke.

        Returns:
            The cached result of the first successful invocation of any
            callable passed to `do` on this `Once` instance.

        Raises:
            TypeError: If `fn` is not callable.
            Exception: Any exception raised by `fn` propagates to the
                caller; in that case the run is not recorded as done.
        """
        if not callable(fn):
            raise TypeError("fn must be callable")

        # Fast path: already completed successfully.
        if self._done:
            return self._value

        with self._lock:
            # Double-checked: another thread may have completed it while
            # we were waiting for the lock.
            if self._done:
                return self._value

            # Run fn outside of marking as done; if it raises, `_done`
            # remains False so a future call may retry.
            result = fn()

            # Only record success after fn returns without raising.
            self._value = result
            self._done = True
            return self._value
