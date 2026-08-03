import threading
import time

import pytest

from src.solution import PhaseBarrier


def test_bad_parties_raises():
    with pytest.raises(ValueError):
        PhaseBarrier(0)
    with pytest.raises(ValueError):
        PhaseBarrier(-2)


def test_timeout_before_all_arrive():
    b = PhaseBarrier(2)
    start = time.monotonic()
    with pytest.raises(TimeoutError):
        b.wait(timeout=0.1)
    assert time.monotonic() - start >= 0.08
    assert b.n_waiting() == 0


def test_barrier_is_cyclic_across_many_phases():
    # A non-reusable barrier would deadlock on the second phase and time out.
    parties = 3
    phases = 5
    b = PhaseBarrier(parties)
    counts = [0] * phases
    counts_lock = threading.Lock()

    def worker():
        for p in range(phases):
            b.wait(timeout=10)
            with counts_lock:
                counts[p] += 1

    threads = [threading.Thread(target=worker) for _ in range(parties)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=15)
    assert all(not t.is_alive() for t in threads)
    assert counts == [parties] * phases
    assert b.n_waiting() == 0
