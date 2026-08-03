import threading
import time

import pytest

from src.solution import BoundedBlockingQueue


def test_fifo_order_preserved():
    q = BoundedBlockingQueue(5)
    for x in range(5):
        assert q.put(x) is True
    assert q.size() == 5
    assert [q.get() for _ in range(5)] == [0, 1, 2, 3, 4]
    assert q.size() == 0


def test_get_times_out_when_empty():
    q = BoundedBlockingQueue(2)
    start = time.monotonic()
    with pytest.raises(TimeoutError):
        q.get(timeout=0.1)
    assert time.monotonic() - start >= 0.08


def test_get_blocks_until_item_available():
    q = BoundedBlockingQueue(2)
    got = threading.Event()
    result = {}

    def consumer():
        result["val"] = q.get(timeout=5)
        got.set()

    t = threading.Thread(target=consumer)
    t.start()

    assert not got.wait(timeout=0.15)
    q.put("hello")
    assert got.wait(timeout=5)
    t.join(timeout=5)
    assert result["val"] == "hello"
