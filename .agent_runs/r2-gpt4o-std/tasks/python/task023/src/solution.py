# src/solution.py

def fib(n, memo={}):
    if n < 0:
        raise ValueError("n must be a non-negative integer")
    if n in memo:
        return memo[n]
    if n == 0:
        return 0
    if n == 1:
        return 1
    memo[n] = fib(n - 1, memo) + fib(n - 2, memo)
    return memo[n]
