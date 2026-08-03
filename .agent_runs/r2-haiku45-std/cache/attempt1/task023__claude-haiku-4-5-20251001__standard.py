# src/solution.py

_memo = {}

def fib(n):
    """
    Returns the nth Fibonacci number (0-indexed) using memoization.
    
    Args:
        n: Non-negative integer index
        
    Returns:
        The nth Fibonacci number
        
    Raises:
        ValueError: If n < 0
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    
    if n in _memo:
        return _memo[n]
    
    if n == 0:
        result = 0
    elif n == 1:
        result = 1
    else:
        result = fib(n - 1) + fib(n - 2)
    
    _memo[n] = result
    return result
