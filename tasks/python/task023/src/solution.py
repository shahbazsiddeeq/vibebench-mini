from __future__ import annotations

# Module-level cache persists across calls, so repeated calls reuse work
# instead of rebuilding the table each time. Filling iteratively avoids
# Python's recursion limit for large n (e.g. fib(1000)).
_memo: dict[int, int] = {0: 0, 1: 1}


def fib(n: int) -> int:
    if n < 0:
        raise ValueError("n must be non-negative")
    if n not in _memo:
        last = max(_memo)
        a, b = _memo[last - 1], _memo[last]
        for k in range(last + 1, n + 1):
            a, b = b, a + b
            _memo[k] = b
    return _memo[n]
