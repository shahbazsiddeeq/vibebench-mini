# src/solution.py

import threading

class RWLock:
    def __init__(self):
        self._readers_lock = threading.Lock()
        self._writers_lock = threading.Lock()
        self._readers_count = 0
        self._writers = 0

    @property
    def active_readers(self):
        with self._readers_lock:
            return self._readers_count

    def acquire_read(self):
        with self._readers_lock:
            if self._writers > 0:
                # Wait until there are no writers
                self._readers_lock.release()
                self._writers_lock.acquire()
                self._readers_lock.acquire()
            self._readers_count += 1

    def release_read(self):
        with self._readers_lock:
            if self._readers_count == 0:
                raise ValueError("No read lock held to release.")
            self._readers_count -= 1
            if self._readers_count == 0:
                # If no readers are left, we can release the writer lock
                self._writers_lock.release()

    def acquire_write(self):
        self._writers_lock.acquire()
        with self._readers_lock:
            self._writers += 1

    def release_write(self):
        with self._readers_lock:
            if self._writers == 0:
                raise ValueError("No write lock held to release.")
            self._writers -= 1
        self._writers_lock.release()
