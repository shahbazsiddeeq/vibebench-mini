_memo = {}

def fib(n: int) -> int:
    """
    Calculates the nth Fibonacci number using memoization.

    Args:
        n: The index of the Fibonacci number to calculate (0-indexed).

    Returns:
        The nth Fibonacci number.

    Raises:
        ValueError: If n is negative.
    """
    if n < 0:
        raise ValueError("Input must be a non-negative integer.")
    if n == 0:
        return 0
    if n == 1:
        return 1
    if n in _memo:
        return _memo[n]

    result = fib(n - 1) + fib(n - 2)
    _memo[n] = result
    return result
