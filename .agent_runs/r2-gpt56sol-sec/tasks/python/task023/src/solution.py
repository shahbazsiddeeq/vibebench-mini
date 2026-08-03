"""Memoized Fibonacci number calculation."""

from __future__ import annotations

import threading

_cache: list[int] = [0, 1]
_cache_lock = threading.Lock()


def fib(n: int) -> int:
    """Return the zero-indexed nth Fibonacci number.

    Args:
        n: A non-negative integer.

    Raises:
        TypeError: If ``n`` is not an integer.
        ValueError: If ``n`` is negative.
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("n must be an integer")
    if n < 0:
        raise ValueError("n must be non-negative")

    with _cache_lock:
        while len(_cache) <= n:
            _cache.append(_cache[-1] + _cache[-2])
        return _cache[n]
