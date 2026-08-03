import sys
import threading

import pytest

from src.solution import TokenBucket


def test_starts_full_and_consumes():
    b = TokenBucket(2)
    assert b.allow() is True
    assert b.allow() is True
    assert b.allow() is False


def test_refill_capped_at_capacity():
    b = TokenBucket(2)
    b.allow(2)
    b.refill(5)
    assert b.tokens == 2
    assert b.allow(2) is True
    assert b.allow() is False


def test_invalid_capacity_raises():
    with pytest.raises(ValueError):
        TokenBucket(0)


def test_allow_n_all_or_nothing():
    b = TokenBucket(3)
    assert b.allow(2) is True
    assert b.allow(2) is False  # only 1 left, consumes nothing
    assert b.allow(1) is True


def test_concurrent_allow_total_true_equals_capacity():
    # Far more attempts than tokens, all threads starting together and each
    # looping many times. Without atomic check-and-consume, the TOCTOU race
    # lets more than `capacity` calls succeed (or tokens go negative).
    capacity = 50_000
    n_threads = 8
    attempts_per_thread = 20_000  # 160k attempts >> 50k tokens
    b = TokenBucket(capacity)
    counts = [0] * n_threads
    barrier = threading.Barrier(n_threads)

    def worker(idx):
        barrier.wait()
        c = 0
        for _ in range(attempts_per_thread):
            if b.allow(1):
                c += 1
        counts[idx] = c

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(n_threads)]
    old_interval = sys.getswitchinterval()
    sys.setswitchinterval(1e-6)
    try:
        for t in threads:
            t.start()
        for t in threads:
            t.join()
    finally:
        sys.setswitchinterval(old_interval)

    assert sum(counts) == capacity
    assert b.tokens == 0
