import threading
import time

import pytest

from src.solution import RWLock


def test_read_lock_tracks_active_readers():
    lock = RWLock()
    assert lock.active_readers == 0
    lock.acquire_read()
    assert lock.active_readers == 1
    lock.acquire_read()
    assert lock.active_readers == 2
    lock.release_read()
    assert lock.active_readers == 1
    lock.release_read()
    assert lock.active_readers == 0


def test_write_then_release_allows_readers():
    lock = RWLock()
    lock.acquire_write()
    lock.release_write()
    lock.acquire_read()
    assert lock.active_readers == 1
    lock.release_read()


def test_release_read_without_hold_raises():
    lock = RWLock()
    with pytest.raises(ValueError):
        lock.release_read()


def test_release_write_without_hold_raises():
    lock = RWLock()
    with pytest.raises(ValueError):
        lock.release_write()


def test_reader_holds_while_writer_waits():
    # While a reader holds the lock, a writer must block. A broken lock where
    # readers and writers do not exclude each other lets the writer proceed
    # immediately and fails this test.
    lock = RWLock()
    lock.acquire_read()
    acquired = threading.Event()

    def writer():
        lock.acquire_write()
        acquired.set()
        lock.release_write()

    t = threading.Thread(target=writer)
    t.start()
    # Writer must NOT be able to acquire while the read lock is held.
    assert not acquired.wait(0.15)
    assert lock.active_readers == 1
    # Releasing the read lock lets the waiting writer proceed.
    lock.release_read()
    assert acquired.wait(2.0)
    t.join()


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


def test_multiple_concurrent_readers_do_not_block():
    # Several readers should hold the lock simultaneously.
    lock = RWLock()
    n = 5
    start = threading.Barrier(n)
    peak_seen = threading.Event()

    def reader():
        lock.acquire_read()
        try:
            start.wait(timeout=2.0)
            # All readers are concurrently inside the read section here.
            if lock.active_readers == n:
                peak_seen.set()
        finally:
            lock.release_read()

    threads = [threading.Thread(target=reader) for _ in range(n)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert peak_seen.is_set()
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
