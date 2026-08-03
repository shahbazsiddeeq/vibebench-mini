import sys
import threading

import pytest
from src.solution import AtomicCounter


def test_increment():
    c = AtomicCounter()
    assert c.increment() == 1
    assert c.increment() == 2


def test_decrement():
    c = AtomicCounter(5)
    assert c.decrement() == 4


def test_value():
    c = AtomicCounter(10)
    assert c.value() == 10


def test_negative_initial_raises():
    with pytest.raises(ValueError):
        AtomicCounter(-1)


def test_concurrent_increments_under_contention():
    # A lock-free implementation loses updates when many threads hammer the
    # same counter. Start all workers together (barrier) and have each perform
    # thousands of increments so the read-modify-write race is virtually
    # guaranteed to be lost without proper locking.
    n_threads = 8
    per_thread = 50_000
    c = AtomicCounter()
    barrier = threading.Barrier(n_threads)

    def worker():
        barrier.wait()
        for _ in range(per_thread):
            c.increment()

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

    assert c.value() == n_threads * per_thread


def test_concurrent_mixed_increment_decrement():
    # Balanced increments and decrements must net to exactly zero if every
    # read-modify-write is atomic.
    n_threads = 8
    per_thread = 20_000
    c = AtomicCounter()
    barrier = threading.Barrier(n_threads)

    def up():
        barrier.wait()
        for _ in range(per_thread):
            c.increment()

    def down():
        barrier.wait()
        for _ in range(per_thread):
            c.decrement()

    threads = [threading.Thread(target=up if i % 2 == 0 else down)
               for i in range(n_threads)]
    old_interval = sys.getswitchinterval()
    sys.setswitchinterval(1e-6)
    try:
        for t in threads:
            t.start()
        for t in threads:
            t.join()
    finally:
        sys.setswitchinterval(old_interval)

    assert c.value() == 0
