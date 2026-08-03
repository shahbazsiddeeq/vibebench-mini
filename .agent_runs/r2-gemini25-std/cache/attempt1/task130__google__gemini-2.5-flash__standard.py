import threading

class RWLock:
    def __init__(self):
        self._read_ready = threading.Condition(threading.Lock())
        self._readers = 0
        self._writers_waiting = 0
        self._writer_active = False

    @property
    def active_readers(self):
        with self._read_ready:
            return self._readers

    def acquire_read(self):
        with self._read_ready:
            while self._writer_active or self._writers_waiting > 0:
                self._read_ready.wait()
            self._readers += 1

    def release_read(self):
        with self._read_ready:
            if self._readers == 0:
                raise ValueError("Cannot release read lock: no read lock held.")
            self._readers -= 1
            if self._readers == 0:
                self._read_ready.notify_all()

    def acquire_write(self):
        with self._read_ready:
            self._writers_waiting += 1
            while self._readers > 0 or self._writer_active:
                self._read_ready.wait()
            self._writers_waiting -= 1
            self._writer_active = True

    def release_write(self):
        with self._read_ready:
            if not self._writer_active:
                raise ValueError("Cannot release write lock: no write lock held.")
            self._writer_active = False
            self._read_ready.notify_all()
