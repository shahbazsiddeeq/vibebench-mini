import threading
import time

import pytest

from src.solution import BoundedBlockingQueue


def test_bad_capacity_raises():
    with pytest.raises(ValueError):
        BoundedBlockingQueue(0)
    with pytest.raises(ValueError):
        BoundedBlockingQueue(-3)


def test_put_nonblocking_when_full_returns_false():
    q = BoundedBlockingQueue(1)
    assert q.put("a", timeout=0) is True
    start = time.monotonic()
    assert q.put("b", timeout=0.1) is False
    assert time.monotonic() - start >= 0.08
    assert q.size() == 1


def test_put_blocks_until_slot_freed():
    # A queue that does not enforce the bound would let the second put finish
    # immediately, tripping the "still blocked" assertion.
    q = BoundedBlockingQueue(1)
    assert q.put("first") is True

    done = threading.Event()
    result = {}

    def producer():
        result["ok"] = q.put("second", timeout=5)
        done.set()

    t = threading.Thread(target=producer)
    t.start()

    # The producer must stay blocked while the queue is full.
    assert not done.wait(timeout=0.15)
    assert q.size() == 1

    # Freeing a slot must release the blocked producer.
    assert q.get() == "first"
    assert done.wait(timeout=5)
    t.join(timeout=5)
    assert result["ok"] is True
    assert q.get() == "second"


def test_concurrent_producers_consumers_lose_nothing():
    q = BoundedBlockingQueue(4)
    n_producers = 4
    per = 250
    consumed = []
    consumed_lock = threading.Lock()
    total = n_producers * per
    start = threading.Barrier(n_producers + 2)  # 4 producers + 2 consumers

    def producer(pid):
        start.wait()
        for i in range(per):
            assert q.put((pid, i), timeout=10) is True

    def consumer():
        start.wait()
        while True:
            item = q.get(timeout=10)
            if item is None:
                return
            with consumed_lock:
                consumed.append(item)

    producers = [
        threading.Thread(target=producer, args=(pid,)) for pid in range(n_producers)
    ]
    consumers = [threading.Thread(target=consumer) for _ in range(2)]
    for t in producers + consumers:
        t.start()

    for t in producers:
        t.join(timeout=20)
    # Sentinels to stop the two consumers once all real items are produced.
    q.put(None, timeout=10)
    q.put(None, timeout=10)
    for t in consumers:
        t.join(timeout=20)

    assert len(consumed) == total
    assert set(consumed) == {(pid, i) for pid in range(n_producers) for i in range(per)}
    assert q.size() == 0
