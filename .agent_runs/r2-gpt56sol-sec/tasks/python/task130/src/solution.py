"""Thread-safe read-write lock implementation."""

from __future__ import annotations

import threading
from typing import Dict, Optional


class RWLock:
    """A writer-preferring, non-reentrant write lock with shared readers."""

    def __init__(self) -> None:
        self._condition = threading.Condition(threading.Lock())
        self._reader_counts: Dict[threading.Thread, int] = {}
        self._active_readers = 0
        self._writer: Optional[threading.Thread] = None
        self._waiting_writers = 0

    @property
    def active_readers(self) -> int:
        """Return the number of currently held read locks."""
        with self._condition:
            return self._active_readers

    def acquire_read(self) -> None:
        """Acquire a shared read lock, blocking while necessary."""
        current = threading.current_thread()

        with self._condition:
            if self._writer is current:
                raise ValueError("cannot acquire a read lock while holding the write lock")

            current_count = self._reader_counts.get(current, 0)

            # Existing readers may acquire recursively. New readers yield to
            # waiting writers to prevent indefinite writer starvation.
            while self._writer is not None or (
                self._waiting_writers > 0 and current_count == 0
            ):
                self._condition.wait()
                current_count = self._reader_counts.get(current, 0)

            self._reader_counts[current] = current_count + 1
            self._active_readers += 1

    def release_read(self) -> None:
        """Release one read lock held by the calling thread."""
        current = threading.current_thread()

        with self._condition:
            count = self._reader_counts.get(current, 0)
            if count == 0:
                raise ValueError("read lock is not held by the current thread")

            if count == 1:
                del self._reader_counts[current]
            else:
                self._reader_counts[current] = count - 1

            self._active_readers -= 1
            if self._active_readers == 0:
                self._condition.notify_all()

    def acquire_write(self) -> None:
        """Acquire the exclusive write lock, blocking while necessary."""
        current = threading.current_thread()

        with self._condition:
            if self._writer is current:
                raise ValueError("write lock is not reentrant")
            if self._reader_counts.get(current, 0) > 0:
                raise ValueError("cannot acquire the write lock while holding a read lock")

            self._waiting_writers += 1
            try:
                while self._writer is not None or self._active_readers > 0:
                    self._condition.wait()
                self._writer = current
            finally:
                self._waiting_writers -= 1
                self._condition.notify_all()

    def release_write(self) -> None:
        """Release the write lock held by the calling thread."""
        current = threading.current_thread()

        with self._condition:
            if self._writer is not current:
                raise ValueError("write lock is not held by the current thread")

            self._writer = None
            self._condition.notify_all()
