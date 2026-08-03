import sys
import threading
import time

import pytest

from src.solution import Bank


def test_basic_transfer():
    bank = Bank({"a": 100, "b": 0})
    assert bank.transfer("a", "b", 30) is True
    assert bank.balance("a") == 70
    assert bank.balance("b") == 30
    assert bank.total() == 100


def test_unknown_account_raises_keyerror():
    bank = Bank({"a": 1, "b": 2})
    with pytest.raises(KeyError):
        bank.transfer("a", "z", 1)
    with pytest.raises(KeyError):
        bank.transfer("z", "a", 1)
    with pytest.raises(KeyError):
        bank.balance("z")


def test_no_deadlock_under_opposing_transfers():
    # Many threads run opposing transfers (a<->b, c<->d) concurrently. An
    # implementation that locks accounts in transfer order (src then dst)
    # instead of a fixed global order will deadlock; a correct one that always
    # locks in a consistent order will not. A tiny thread-switch interval makes
    # the deadlock interleaving reliable for a broken implementation, while the
    # correct implementation stays live no matter how often threads are switched.
    old_interval = sys.getswitchinterval()
    sys.setswitchinterval(1e-6)
    try:
        pairs = [("a", "b"), ("c", "d")]
        bank = Bank({name: 1_000_000 for pair in pairs for name in pair})
        iters = 20_000
        n_workers = 8
        start = threading.Barrier(n_workers)

        def worker(wid):
            x, y = pairs[wid % len(pairs)]
            # Half the workers push x->y, the other half push y->x: opposing
            # lock-acquisition orders, the classic deadlock setup.
            src, dst = (x, y) if (wid // len(pairs)) % 2 == 0 else (y, x)
            start.wait()
            for _ in range(iters):
                bank.transfer(src, dst, 1)

        # daemon=True so a genuinely deadlocked (broken) implementation still
        # lets the interpreter exit after this test reports failure.
        threads = [
            threading.Thread(target=worker, args=(w,), daemon=True)
            for w in range(n_workers)
        ]
        for t in threads:
            t.start()
        # Single shared deadline so a deadlocked (broken) implementation is
        # reported quickly instead of paying the timeout once per thread.
        deadline = time.monotonic() + 20
        for t in threads:
            t.join(timeout=max(0.0, deadline - time.monotonic()))
        assert all(not t.is_alive() for t in threads), "transfers deadlocked"
        assert bank.total() == 4_000_000
    finally:
        sys.setswitchinterval(old_interval)


def test_no_overdraft_race():
    # Two threads race to drain the same account; combined they must not
    # withdraw more than exists, so the destination cannot exceed the source's
    # starting balance and the source can never go negative.
    for _ in range(1):
        bank = Bank({"src": 100, "dst": 0})
        n_threads = 8
        start = threading.Barrier(n_threads)

        def worker():
            start.wait()
            for _ in range(400):
                bank.transfer("src", "dst", 1)

        threads = [threading.Thread(target=worker) for _ in range(n_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=30)
        assert bank.balance("src") == 0
        assert bank.balance("dst") == 100
        assert bank.total() == 100
