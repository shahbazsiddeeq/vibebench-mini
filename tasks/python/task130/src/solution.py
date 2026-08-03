import threading


class RWLock:
    """A readers-writer lock: many readers or one exclusive writer."""

    def __init__(self):
        self._cond = threading.Condition(threading.Lock())
        self._readers = 0
        self._writer = False

    def acquire_read(self) -> None:
        with self._cond:
            while self._writer:
                self._cond.wait()
            self._readers += 1

    def release_read(self) -> None:
        with self._cond:
            if self._readers <= 0:
                raise ValueError("release_read called without a held read lock")
            self._readers -= 1
            if self._readers == 0:
                self._cond.notify_all()

    def acquire_write(self) -> None:
        with self._cond:
            while self._writer or self._readers > 0:
                self._cond.wait()
            self._writer = True

    def release_write(self) -> None:
        with self._cond:
            if not self._writer:
                raise ValueError("release_write called without a held write lock")
            self._writer = False
            self._cond.notify_all()

    @property
    def active_readers(self) -> int:
        with self._cond:
            return self._readers
