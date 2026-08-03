"""
src/solution.py

A thread-safe Read-Write Lock implementation.

This module provides an RWLock class allowing multiple concurrent readers
or a single exclusive writer. It uses only the Python standard library
(threading) and avoids any use of eval/exec or external randomness needs.

Design notes (security / robustness):
- All state mutations are protected by an internal threading.Condition,
  ensuring no race conditions corrupt the lock's internal bookkeeping.
- release_read()/release_write() validate that the calling thread actually
  holds the corresponding lock before releasing it, raising ValueError
  otherwise (never silently corrupting internal state).
- No external/untrusted input is processed by this module, so there is no
  need for input sanitization beyond internal consistency checks.
- No secrets or randomness are required for this synchronization primitive.
"""

import threading
from typing import Dict, Optional


class RWLock:
    """
    A simple reader-writer lock.

    Multiple threads may hold the lock for reading simultaneously, but
    only one thread may hold it for writing, and no readers may hold it
    while a writer does.
    """

    def __init__(self) -> None:
        self._cond = threading.Condition(threading.Lock())
        self._readers: int = 0
        self._writer: bool = False
        self._writer_owner: Optional[int] = None
        self._reader_counts: Dict[int, int] = {}

    @property
    def active_readers(self) -> int:
        """Return the current number of active readers."""
        with self._cond:
            return self._readers

    def acquire_read(self) -> None:
        """Acquire the lock for reading, blocking while a writer holds it."""
        with self._cond:
            while self._writer:
                self._cond.wait()
            self._readers += 1
            tid = threading.get_ident()
            self._reader_counts[tid] = self._reader_counts.get(tid, 0) + 1

    def release_read(self) -> None:
        """
        Release a previously acquired read lock.

        Raises:
            ValueError: if the calling thread does not currently hold a
                read lock acquired via acquire_read().
        """
        with self._cond:
            tid = threading.get_ident()
            count = self._reader_counts.get(tid, 0)
            if count <= 0:
                raise ValueError(
                    "release_read() called without a matching acquire_read()"
                )
            if count == 1:
                del self._reader_counts[tid]
            else:
                self._reader_counts[tid] = count - 1

            if self._readers <= 0:
                # Should not happen given the guard above, but keep state safe.
                raise ValueError(
                    "release_read() called without a matching acquire_read()"
                )
            self._readers -= 1
            if self._readers == 0:
                self._cond.notify_all()

    def acquire_write(self) -> None:
        """Acquire the lock exclusively, blocking until no readers/writers hold it."""
        with self._cond:
            while self._writer or self._readers > 0:
                self._cond.wait()
            self._writer = True
            self._writer_owner = threading.get_ident()

    def release_write(self) -> None:
        """
        Release a previously acquired write lock.

        Raises:
            ValueError: if the calling thread does not currently hold the
                write lock acquired via acquire_write().
        """
        with self._cond:
            tid = threading.get_ident()
            if not self._writer or self._writer_owner != tid:
                raise ValueError(
                    "release_write() called without a matching acquire_write()"
                )
            self._writer = False
            self._writer_owner = None
            self._cond.notify_all()
