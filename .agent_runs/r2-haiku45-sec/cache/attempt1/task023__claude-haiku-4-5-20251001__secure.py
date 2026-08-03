"""
Fibonacci implementation with memoization.
"""

_fib_cache = {}


def fib(n: int) -> int:
    """
    Returns the nth Fibonacci number (0-indexed).
    
    fib(0) = 0
    fib(1) = 1
    fib(n) = fib(n-1) + fib(n-2) for n > 1
    
    Uses memoization to cache results across calls.
    
    Args:
        n: Non-negative integer index
        
    Returns:
        The nth Fibonacci number
        
    Raises:
        ValueError: If n < 0
    """
    # Input validation
    if not isinstance(n, int):
        raise ValueError("n must be an integer")
    if n < 0:
        raise ValueError("n must be non-negative")
    
    # Check cache first
    if n in _fib_cache:
        return _fib_cache[n]
    
    # Base cases
    if n == 0:
        result = 0
    elif n == 1:
        result = 1
    else:
        # Recursive case with memoization
        result = fib(n - 1) + fib(n - 2)
    
    # Store in cache
    _fib_cache[n] = result
    return result
