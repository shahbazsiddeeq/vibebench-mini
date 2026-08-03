import sys
import threading
import time

import pytest

from src.solution import Once


def test_subsequent_calls_return_cached():
    o = Once()
    assert o.do(lambda: 5) == 5
    assert o.do(lambda: 99) == 5


def test_caches_none_result():
    o = Once()
    assert o.do(lambda: None) is None
    # fn should not run again even though the cached value is falsy.
    assert o.do(lambda: 42) is None


def test_concurrent_do_runs_fn_once():
    o = Once()
    counter = {"value": 0}
    lock = threading.Lock()

    def init():
        with lock:
            counter["value"] += 1
        time.sleep(0.001)
        return "initialized"

    n_threads = 64
    barrier = threading.Barrier(n_threads)
    returned = []
    returned_lock = threading.Lock()

    def worker():
        barrier.wait()  # release all threads simultaneously
        value = o.do(init)
        with returned_lock:
            returned.append(value)

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

    assert counter["value"] == 1
    assert all(v == "initialized" for v in returned)
    assert len(returned) == n_threads
