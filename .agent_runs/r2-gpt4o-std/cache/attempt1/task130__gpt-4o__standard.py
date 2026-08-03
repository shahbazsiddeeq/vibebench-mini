# src/solution.py

import threading

class RWLock:
    def __init__(self):
        self._readers = 0
        self._readers_lock = threading.Lock()
        self._writers_lock = threading.Lock()
        self._readers_waiting = threading.Condition(self._readers_lock)

    @property
    def active_readers(self):
        with self._readers_lock:
            return self._readers

    def acquire_read(self):
        with self._readers_waiting:
            while self._writers_lock.locked():
                self._readers_waiting.wait()
            self._readers += 1

    def release_read(self):
        with self._readers_lock:
            if self._readers == 0:
                raise ValueError("No read lock held")
            self._readers -= 1
            if self._readers == 0:
                with self._readers_waiting:
                    self._readers_waiting.notify_all()

    def acquire_write(self):
        self._writers_lock.acquire()

    def release_write(self):
        if not self._writers_lock.locked():
            raise ValueError("No write lock held")
        self._writers_lock.release()
        with self._readers_waiting:
            self._readers_waiting.notify_all()
