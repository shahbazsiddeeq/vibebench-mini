import threading

class RWLock:
    def __init__(self):
        self._read_lock = threading.Lock()
        self._write_lock = threading.Lock()
        self._active_readers = 0
        self._write_count = 0
        self._read_count = 0

    @property
    def active_readers(self):
        return self._active_readers

    def acquire_read(self):
        with self._read_lock:
            if self._write_count > 0:
                # Wait until there are no writers
                self._read_lock.release()
                self._write_lock.acquire()
                self._write_lock.release()
                self._read_lock.acquire()
            self._active_readers += 1

    def release_read(self):
        with self._read_lock:
            if self._active_readers == 0:
                raise ValueError("No active readers to release")
            self._active_readers -= 1

    def acquire_write(self):
        self._write_lock.acquire()
        with self._read_lock:
            self._write_count += 1

    def release_write(self):
        with self._read_lock:
            if self._write_count == 0:
                raise ValueError("No active writer to release")
            self._write_count -= 1
        self._write_lock.release()
