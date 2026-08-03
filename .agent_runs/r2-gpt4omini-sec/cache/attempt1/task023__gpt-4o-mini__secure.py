# src/solution.py

def fib(n: int) -> int:
    if not isinstance(n, int) or n < 0:
        raise ValueError("Input must be a non-negative integer.")
    
    memo = {}

    def _fib(n: int) -> int:
        if n in memo:
            return memo[n]
        if n == 0:
            return 0
        if n == 1:
            return 1
        memo[n] = _fib(n - 1) + _fib(n - 2)
        return memo[n]

    return _fib(n)
