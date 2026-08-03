import threading
import time

import pytest

from src.solution import CountDownLatch


def test_count_down_decrements():
    latch = CountDownLatch(2)
    latch.count_down()
    assert latch.get_count() == 1
    latch.count_down()
    assert latch.get_count() == 0


def test_negative_count_raises():
    with pytest.raises(ValueError):
        CountDownLatch(-1)


def test_await_times_out_while_count_positive():
    latch = CountDownLatch(1)
    start = time.monotonic()
    assert latch.await_latch(timeout=0.1) is False
    assert time.monotonic() - start >= 0.08
    assert latch.get_count() == 1


def test_await_after_zero_is_immediate_true():
    latch = CountDownLatch(1)
    latch.count_down()
    assert latch.await_latch() is True
    assert latch.await_latch(timeout=0) is True
