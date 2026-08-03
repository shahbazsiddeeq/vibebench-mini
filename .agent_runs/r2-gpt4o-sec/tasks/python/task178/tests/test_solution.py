import threading
import time

import pytest

from src.solution import PhaseBarrier


def test_bad_parties_raises():
    with pytest.raises(ValueError):
        PhaseBarrier(0)
    with pytest.raises(ValueError):
        PhaseBarrier(-2)


def test_parties_attribute_and_single_party_passthrough():
    b = PhaseBarrier(1)
    assert b.parties == 1
    assert b.wait() == 0
    assert b.wait() == 0  # reusable for the next phase


def test_timeout_before_all_arrive():
    b = PhaseBarrier(2)
    start = time.monotonic()
    with pytest.raises(TimeoutError):
        b.wait(timeout=0.1)
    assert time.monotonic() - start >= 0.08
    assert b.n_waiting() == 0


def test_no_thread_returns_until_all_arrive():
    # A barrier that releases early (before all parties arrive) would set some
    # `released` events during the pre-arrival window and fail the assertion.
    parties = 4
    b = PhaseBarrier(parties)
    released = [threading.Event() for _ in range(parties)]
    indices = [None] * parties

    def worker(i):
        idx = b.wait(timeout=5)
        indices[i] = idx
        released[i].set()

    # Start parties - 1 threads; they must all stay blocked.
    threads = [threading.Thread(target=worker, args=(i,)) for i in range(parties - 1)]
    for t in threads:
        t.start()

    # Wait for them to actually be blocked in wait().
    deadline = time.monotonic() + 5
    while b.n_waiting() < parties - 1 and time.monotonic() < deadline:
        time.sleep(0.005)
    assert b.n_waiting() == parties - 1
    assert not any(e.is_set() for e in released)

    # The final arrival must release everyone together.
    last = threading.Thread(target=worker, args=(parties - 1,))
    last.start()
    threads.append(last)
    for t in threads:
        t.join(timeout=5)
    assert all(not t.is_alive() for t in threads)
    assert all(e.is_set() for e in released)
    # Every arrival index in the phase is distinct and covers 0..parties-1.
    assert sorted(indices) == list(range(parties))


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


def test_all_parties_synchronize_each_phase():
    # Detects an implementation that lets a fast thread lap the others: record
    # the max phase any thread has entered vs. min phase; they must stay in lock
    # step (differ by at most one across the barrier boundary).
    parties = 4
    phases = 20
    b = PhaseBarrier(parties)
    progress = [0] * parties

    def worker(i):
        for p in range(phases):
            progress[i] = p
            b.wait(timeout=10)
            # After the barrier, no peer can be more than one phase behind.
            assert max(progress) - min(progress) <= 1

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(parties)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=20)
    assert all(not t.is_alive() for t in threads)
