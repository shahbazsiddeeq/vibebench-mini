"""Memoized Fibonacci implementation."""

_cache = {0: 0, 1: 1}


def fib(n: int) -> int:
    """Return the nth Fibonacci number using a persistent memoization cache."""
    if not isinstance(n, int):
        raise TypeError("n must be an integer")
    if n < 0:
        raise ValueError("n must be non-negative")

    if n not in _cache:
        highest = max(_cache)
        previous, current = _cache[highest - 1], _cache[highest]
        for index in range(highest + 1, n + 1):
            previous, current = current, previous + current
            _cache[index] = current

    return _cache[n]
