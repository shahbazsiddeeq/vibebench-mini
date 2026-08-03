def fib(n):
    """
    Returns the nth Fibonacci number (0-indexed) using memoization.
    
    Args:
        n: The index of the Fibonacci number to compute (0-indexed)
        
    Returns:
        The nth Fibonacci number
        
    Raises:
        ValueError: If n is negative
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    
    if not hasattr(fib, '_memo'):
        fib._memo = {}
    
    if n in fib._memo:
        return fib._memo[n]
    
    if n == 0:
        result = 0
    elif n == 1:
        result = 1
    else:
        result = fib(n - 1) + fib(n - 2)
    
    fib._memo[n] = result
    return result
