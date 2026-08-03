"""
Fibonacci (Memoized) module.

Provides a secure, self-contained implementation of a memoized
Fibonacci function. Only standard library is used.
"""

from functools import lru_cache
from typing import Union


@lru_cache(maxsize=None)
def _fib_helper(n: int) -> int:
    """Internal memoized Fibonacci computation.

    Assumes n is a non-negative integer; validation happens in fib().
    """
    if n == 0:
        return 0
    if n == 1:
        return 1

    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def fib(n: Union[int, bool]) -> int:
    """Return the nth Fibonacci number (0-indexed) using memoization.

    fib(0) == 0, fib(1) == 1

    Args:
        n: A non-negative integer index.

    Returns:
        The nth Fibonacci number as an int.

    Raises:
        ValueError: If n is not an integer or is negative.
    """
    # Reject bool explicitly since bool is a subclass of int in Python.
    if isinstance(n, bool):
        raise ValueError("n must be a non-negative integer, not a boolean")

    if not isinstance(n, int):
        raise ValueError("n must be an integer")

    if n < 0:
        raise ValueError("n must be a non-negative integer")

    return _fib_helper(n)
