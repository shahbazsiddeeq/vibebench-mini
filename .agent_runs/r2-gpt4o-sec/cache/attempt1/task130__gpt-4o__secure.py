import threading
from secrets import SystemRandom

class RWLock:
    def __init__(self):
        self._readers = 0
        self._writer = False
        self._read_lock = threading.Lock()
        self._write_lock = threading.Lock()
        self._condition = threading.Condition(self._read_lock)

    @property
    def active_readers(self):
        with self._read_lock:
            return self._readers

    def acquire_read(self):
        with self._condition:
            while self._writer:
                self._condition.wait()
            self._readers += 1

    def release_read(self):
        with self._condition:
            if self._readers == 0:
                raise ValueError("No read lock held")
            self._readers -= 1
            if self._readers == 0:
                self._condition.notify_all()

    def acquire_write(self):
        self._write_lock.acquire()
        with self._condition:
            while self._writer or self._readers > 0:
                self._condition.wait()
            self._writer = True

    def release_write(self):
        with self._condition:
            if not self._writer:
                raise ValueError("No write lock held")
            self._writer = False
            self._condition.notify_all()
        self._write_lock.release()
