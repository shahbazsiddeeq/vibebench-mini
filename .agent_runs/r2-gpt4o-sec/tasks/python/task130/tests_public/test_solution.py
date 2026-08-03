import threading
import time

import pytest

from src.solution import RWLock


def test_write_then_release_allows_readers():
    lock = RWLock()
    lock.acquire_write()
    lock.release_write()
    lock.acquire_read()
    assert lock.active_readers == 1
    lock.release_read()


def test_release_write_without_hold_raises():
    lock = RWLock()
    with pytest.raises(ValueError):
        lock.release_write()


def test_writer_blocks_new_readers():
    # While a writer holds the lock, readers must block until it is released.
    lock = RWLock()
    lock.acquire_write()
    got_read = threading.Event()

    def reader():
        lock.acquire_read()
        got_read.set()
        lock.release_read()

    t = threading.Thread(target=reader)
    t.start()
    assert not got_read.wait(0.15)
    lock.release_write()
    assert got_read.wait(2.0)
    t.join()
    assert lock.active_readers == 0


def test_concurrent_writers_no_lost_updates():
    lock = RWLock()
    shared = []

    def writer(start):
        for i in range(50):
            lock.acquire_write()
            try:
                # Mutation guarded exclusively by the write lock.
                current = list(shared)
                time.sleep(0.001)
                current.append(start + i)
                shared.clear()
                shared.extend(current)
            finally:
                lock.release_write()

    threads = [threading.Thread(target=writer, args=(base * 1000,)) for base in range(6)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert len(shared) == 6 * 50
    assert lock.active_readers == 0
