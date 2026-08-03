import functools
from typing import Dict


@functools.lru_cache(maxsize=None)
def fib(n: int) -> int:
    """
    Returns the nth Fibonacci number (0-indexed).
    
    Args:
        n: The index of the Fibonacci number to compute (must be >= 0)
        
    Returns:
        The nth Fibonacci number
        
    Raises:
        ValueError: If n < 0
    """
    # Validate input
    if not isinstance(n, int):
        raise TypeError("n must be an integer")
    
    if n < 0:
        raise ValueError("n must be non-negative")
    
    # Base cases
    if n == 0:
        return 0
    if n == 1:
        return 1
    
    # Recursive case with memoization via lru_cache
    return fib(n - 1) + fib(n - 2)
