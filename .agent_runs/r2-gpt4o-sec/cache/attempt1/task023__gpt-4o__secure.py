# src/solution.py

def fib(n):
    if not isinstance(n, int):
        raise TypeError("Input must be an integer.")
    if n < 0:
        raise ValueError("Input must be a non-negative integer.")
    
    memo = {}

    def fib_memo(n):
        if n in memo:
            return memo[n]
        if n == 0:
            result = 0
        elif n == 1:
            result = 1
        else:
            result = fib_memo(n - 1) + fib_memo(n - 2)
        memo[n] = result
        return result

    return fib_memo(n)
