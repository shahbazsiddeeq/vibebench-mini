"""
src/solution.py

A thread-safe CountDownLatch implementation.

This module provides a single class, ``CountDownLatch``, which mirrors the
behaviour of similar constructs found in other languages/libraries (e.g.
Java's ``java.util.concurrent.CountDownLatch``). It allows one or more
threads to wait until a set of operations being performed in other threads
completes.

Security / robustness notes:
    * All public inputs are validated defensively.
    * No use of eval/exec or dynamic code execution.
    * No external I/O is performed.
    * Internal state is protected by a threading.Condition to ensure
      correct behaviour under concurrent access, and no internal state
      or tracebacks are leaked to callers on error -- only well-defined
      exceptions with safe messages are raised.
"""

from __future__ import annotations

import threading
from typing import Optional


class CountDownLatch:
    """A one-shot, thread-safe count-down latch.

    Parameters
    ----------
    count:
        The initial count. Must be a non-negative integer.

    Raises
    ------
    ValueError
        If ``count`` is negative or not an integer.
    """

    def __init__(self, count: int) -> None:
        # Validate input type strictly: bool is a subclass of int, but we
        # don't want to silently accept True/False as counts, so exclude it
        # explicitly for clarity and to avoid subtle bugs.
        if isinstance(count, bool) or not isinstance(count, int):
            raise ValueError("count must be a non-negative integer")
        if count < 0:
            raise ValueError("count must be a non-negative integer")

        self._count = count
        self._condition = threading.Condition(threading.Lock())

    def count_down(self) -> None:
        """Decrement the internal counter by one, never below zero.

        If the count is already zero, this call is a no-op. When the
        count transitions from 1 to 0, all threads currently blocked in
        :meth:`await_latch` are released.
        """
        with self._condition:
            if self._count > 0:
                self._count -= 1
                if self._count == 0:
                    self._condition.notify_all()

    def await_latch(self, timeout: Optional[float] = None) -> bool:
        """Block until the count reaches zero, or until ``timeout`` elapses.

        Parameters
        ----------
        timeout:
            Maximum number of seconds to wait. ``None`` (the default)
            means wait indefinitely. Must be ``None`` or a non-negative
            number.

        Returns
        -------
        bool
            ``True`` if the count reached zero before the timeout
            expired (or immediately, if it was already zero), ``False``
            if the timeout elapsed first.

        Raises
        ------
        ValueError
            If ``timeout`` is negative or not a valid numeric type.
        """
        if timeout is not None:
            if isinstance(timeout, bool) or not isinstance(timeout, (int, float)):
                raise ValueError("timeout must be a non-negative number or None")
            if timeout < 0:
                raise ValueError("timeout must be a non-negative number or None")

        with self._condition:
            if self._count == 0:
                return True

            if timeout is None:
                # Wait indefinitely, guarding against spurious wakeups.
                while self._count != 0:
                    self._condition.wait()
                return True

            # Bounded wait: track remaining time across spurious wakeups.
            deadline = _monotonic() + timeout
            remaining = timeout
            while self._count != 0:
                if remaining <= 0:
                    return False
                self._condition.wait(timeout=remaining)
                remaining = deadline - _monotonic()

            return True

    def get_count(self) -> int:
        """Return the current value of the counter."""
        with self._condition:
            return self._count


def _monotonic() -> float:
    """Small wrapper around time.monotonic to keep imports localized."""
    import time

    return time.monotonic()
