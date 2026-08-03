# src/solution.py

def fib(n, memo=None):
    if n < 0:
        raise ValueError("n must be a non-negative integer")
    
    if memo is None:
        memo = {}
    
    if n in memo:
        return memo[n]
    
    if n == 0:
        result = 0
    elif n == 1:
        result = 1
    else:
        result = fib(n - 1, memo) + fib(n - 2, memo)
    
    memo[n] = result
    return result
