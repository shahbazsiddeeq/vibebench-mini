import functools

@functools.lru_cache(maxsize=None)
def fib(n: int) -> int:
    """
    Calculates the nth Fibonacci number using memoization.

    Args:
        n: The index of the Fibonacci number to calculate (0-indexed).

    Returns:
        The nth Fibonacci number.

    Raises:
        ValueError: If n is a negative integer.
    """
    if not isinstance(n, int):
        raise TypeError("Input 'n' must be an integer.")
    if n < 0:
        raise ValueError("Input 'n' cannot be negative.")
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)
