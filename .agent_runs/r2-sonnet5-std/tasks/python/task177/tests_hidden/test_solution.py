import threading
import time

import pytest

from src.solution import ResourcePool


def test_bad_capacity_raises():
    with pytest.raises(ValueError):
        ResourcePool(0)
    with pytest.raises(ValueError):
        ResourcePool(-1)


def test_acquire_nonblocking_when_exhausted():
    pool = ResourcePool(1)
    assert pool.acquire(timeout=0) is True
    start = time.monotonic()
    assert pool.acquire(timeout=0.1) is False
    assert time.monotonic() - start >= 0.08
    assert pool.available() == 0


def test_blocked_acquire_released_on_release():
    pool = ResourcePool(1)
    assert pool.acquire() is True
    done = threading.Event()
    result = {}

    def worker():
        result["ok"] = pool.acquire(timeout=5)
        done.set()

    t = threading.Thread(target=worker)
    t.start()
    assert not done.wait(timeout=0.15)
    assert pool.available() == 0
    pool.release()
    assert done.wait(timeout=5)
    t.join(timeout=5)
    assert result["ok"] is True


def test_slot_context_manager_releases():
    pool = ResourcePool(1)
    with pool.slot():
        assert pool.available() == 0
    assert pool.available() == 1
