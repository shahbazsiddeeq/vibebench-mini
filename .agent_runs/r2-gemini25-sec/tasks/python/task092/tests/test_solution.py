import sys
import threading

from src.solution import memoize


def test_basic_caching():
    call_count = [0]

    @memoize
    def add(a, b):
        call_count[0] += 1
        return a + b

    assert add(1, 2) == 3
    assert add(1, 2) == 3
    assert call_count[0] == 1


def test_different_args_not_cached():
    call_count = [0]

    @memoize
    def fn(x):
        call_count[0] += 1
        return x * 2

    fn(1)
    fn(2)
    assert call_count[0] == 2


def test_preserves_name():
    @memoize
    def my_func():
        pass

    assert my_func.__name__ == "my_func"


def test_none_return_cached():
    call_count = [0]

    @memoize
    def fn():
        call_count[0] += 1
        return None

    fn()
    fn()
    assert call_count[0] == 1


def test_keyword_arguments():
    call_count = [0]

    @memoize
    def fn(a, b=0):
        call_count[0] += 1
        return a + b

    assert fn(1, b=2) == 3
    assert fn(1, b=2) == 3
    assert call_count[0] == 1
    # Different keyword value is a distinct key.
    assert fn(1, b=5) == 6
    assert call_count[0] == 2


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


def test_concurrent_first_call_runs_fn_once():
    # Many threads request the same (uncached) key simultaneously; the wrapped
    # function must execute exactly once. A lock-free memoize double-computes.
    lock = threading.Lock()
    call_count = [0]

    @memoize
    def slow(x):
        with lock:
            call_count[0] += 1
        # Widen the race window so a lock-free implementation reliably
        # computes more than once.
        s = 0
        for i in range(20_000):
            s += i
        return x * 2 + (s - s)

    n_threads = 16
    barrier = threading.Barrier(n_threads)
    results = []
    results_lock = threading.Lock()

    def worker():
        barrier.wait()
        r = slow(21)
        with results_lock:
            results.append(r)

    threads = [threading.Thread(target=worker) for _ in range(n_threads)]
    old_interval = sys.getswitchinterval()
    sys.setswitchinterval(1e-6)
    try:
        for t in threads:
            t.start()
        for t in threads:
            t.join()
    finally:
        sys.setswitchinterval(old_interval)

    assert call_count[0] == 1
    assert results == [42] * n_threads
