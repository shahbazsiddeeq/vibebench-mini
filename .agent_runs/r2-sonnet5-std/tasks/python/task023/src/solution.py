from functools import lru_cache


@lru_cache(maxsize=None)
def _fib_helper(n):
    if n < 2:
        return n
    return _fib_helper(n - 1) + _fib_helper(n - 2)


def fib(n):
    if n < 0:
        raise ValueError("n must be non-negative")
    return _fib_helper(n)
