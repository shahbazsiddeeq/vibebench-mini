# src/solution.py

import threading

class RWLock:
    def __init__(self):
        self._readers = 0
        self._writers = 0
        self._readers_lock = threading.Lock()
        self._writers_lock = threading.Lock()
        self._readers_condition = threading.Condition(self._readers_lock)

    @property
    def active_readers(self):
        return self._readers

    def acquire_read(self):
        with self._readers_lock:
            while self._writers > 0:
                self._readers_condition.wait()
            self._readers += 1

    def release_read(self):
        with self._readers_lock:
            if self._readers == 0:
                raise ValueError("No read lock held to release.")
            self._readers -= 1
            if self._readers == 0:
                self._readers_condition.notify_all()

    def acquire_write(self):
        self._writers_lock.acquire()
        with self._readers_lock:
            while self._readers > 0:
                self._readers_condition.wait()
            self._writers += 1

    def release_write(self):
        with self._readers_lock:
            if self._writers == 0:
                self._writers_lock.release()
                raise ValueError("No write lock held to release.")
            self._writers -= 1
            self._readers_condition.notify_all()
        self._writers_lock.release()
