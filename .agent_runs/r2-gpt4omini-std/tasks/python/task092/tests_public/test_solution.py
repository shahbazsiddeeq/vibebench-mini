import sys
import threading

from src.solution import memoize


def test_different_args_not_cached():
    call_count = [0]

    @memoize
    def fn(x):
        call_count[0] += 1
        return x * 2

    fn(1)
    fn(2)
    assert call_count[0] == 2


def test_none_return_cached():
    call_count = [0]

    @memoize
    def fn():
        call_count[0] += 1
        return None

    fn()
    fn()
    assert call_count[0] == 1


def test_recursion_does_not_deadlock():
    call_count = [0]

    @memoize
    def fib(n):
        call_count[0] += 1
        if n < 2:
            return n
        return fib(n - 1) + fib(n - 2)

    assert fib(30) == 832040
    # Each of n = 0..30 computed exactly once thanks to memoization.
    assert call_count[0] == 31
