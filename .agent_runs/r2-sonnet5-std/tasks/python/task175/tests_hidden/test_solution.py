import threading
import time

import pytest

from src.solution import CountDownLatch


def test_get_count_initial():
    assert CountDownLatch(3).get_count() == 3


def test_count_down_clamps_at_zero():
    latch = CountDownLatch(1)
    latch.count_down()
    latch.count_down()
    latch.count_down()
    assert latch.get_count() == 0


def test_await_returns_immediately_when_zero():
    latch = CountDownLatch(0)
    assert latch.await_latch(timeout=1) is True


def test_waiters_release_only_at_zero():
    # A broken latch that releases while count > 0 fails the mid-flight assertion;
    # one that never notifies fails the final all-released assertion.
    parties = 6
    latch = CountDownLatch(3)
    released = [threading.Event() for _ in range(parties)]
    barrier = threading.Barrier(parties)

    def waiter(i):
        barrier.wait()
        if latch.await_latch(timeout=5):
            released[i].set()

    threads = [threading.Thread(target=waiter, args=(i,)) for i in range(parties)]
    for t in threads:
        t.start()

    latch.count_down()
    latch.count_down()
    time.sleep(0.15)
    assert not any(e.is_set() for e in released)
    assert latch.get_count() == 1

    latch.count_down()
    for t in threads:
        t.join(timeout=5)
    assert all(not t.is_alive() for t in threads)
    assert all(e.is_set() for e in released)
