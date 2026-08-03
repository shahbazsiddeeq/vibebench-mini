import threading

class RWLock:
    def __init__(self):
        self._readers = 0
        self._write_lock = threading.Lock()
        self._read_lock = threading.Lock()
        self._readers_lock = threading.Lock()

    @property
    def active_readers(self):
        with self._readers_lock:
            return self._readers

    def acquire_read(self):
        with self._readers_lock:
            if self._readers == 0:
                self._read_lock.acquire()
            self._readers += 1

    def release_read(self):
        with self._readers_lock:
            if self._readers == 0:
                raise ValueError("No read lock held")
            self._readers -= 1
            if self._readers == 0:
                self._read_lock.release()

    def acquire_write(self):
        self._write_lock.acquire()
        self._read_lock.acquire()

    def release_write(self):
        self._read_lock.release()
        self._write_lock.release()
