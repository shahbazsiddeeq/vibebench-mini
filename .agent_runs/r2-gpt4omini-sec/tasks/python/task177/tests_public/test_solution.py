import threading
import time

import pytest

from src.solution import ResourcePool


def test_available_tracks_acquire_release():
    pool = ResourcePool(2)
    assert pool.available() == 2
    assert pool.acquire() is True
    assert pool.available() == 1
    assert pool.acquire() is True
    assert pool.available() == 0
    pool.release()
    assert pool.available() == 1


def test_over_release_raises():
    pool = ResourcePool(2)
    with pytest.raises(ValueError):
        pool.release()
    pool.acquire()
    pool.release()
    with pytest.raises(ValueError):
        pool.release()
    assert pool.available() == 2


def test_peak_concurrency_never_exceeds_capacity():
    # A pool missing its permit accounting would let more than `capacity`
    # threads run at once, tripping the peak assertion.
    capacity = 3
    pool = ResourcePool(capacity)
    n_threads = 24
    start = threading.Barrier(n_threads)

    state_lock = threading.Lock()
    current = {"n": 0}
    peak = {"n": 0}

    def worker():
        start.wait()
        for _ in range(40):
            assert pool.acquire(timeout=10) is True
            with state_lock:
                current["n"] += 1
                if current["n"] > peak["n"]:
                    peak["n"] = current["n"]
                assert current["n"] <= capacity
            time.sleep(0.0005)
            with state_lock:
                current["n"] -= 1
            pool.release()

    threads = [threading.Thread(target=worker) for _ in range(n_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=30)
    assert all(not t.is_alive() for t in threads)
    assert peak["n"] <= capacity
    assert peak["n"] >= 2  # the pool really did run things in parallel
    assert pool.available() == capacity


def test_slot_timeout_raises_and_leaves_state_intact():
    pool = ResourcePool(1)
    with pool.slot():
        with pytest.raises(TimeoutError):
            with pool.slot(timeout=0.1):
                pass
    assert pool.available() == 1
