import threading


class RWLock:
    """A simple readers-writer lock.

    Multiple readers may hold the lock simultaneously via
    acquire_read()/release_read(). A writer has exclusive access via
    acquire_write()/release_write(): while a writer holds the lock, no
    readers and no other writer may hold it; while any reader holds it,
    acquire_write() blocks until all readers release.
    """

    def __init__(self):
        self._lock = threading.Lock()
        self._cond = threading.Condition(self._lock)
        self._readers = 0
        self._writer = False
        self._reader_local = threading.local()
        self._writer_thread = None

    @property
    def active_readers(self):
        with self._lock:
            return self._readers

    def acquire_read(self):
        with self._cond:
            while self._writer:
                self._cond.wait()
            self._readers += 1
            count = getattr(self._reader_local, "count", 0)
            self._reader_local.count = count + 1

    def release_read(self):
        with self._cond:
            count = getattr(self._reader_local, "count", 0)
            if count <= 0:
                raise ValueError("release_read() called without a matching acquire_read()")
            self._reader_local.count = count - 1
            self._readers -= 1
            if self._readers < 0:
                # Shouldn't happen, but guard anyway.
                self._readers = 0
                raise ValueError("release_read() called without a matching acquire_read()")
            if self._readers == 0:
                self._cond.notify_all()

    def acquire_write(self):
        with self._cond:
            while self._writer or self._readers > 0:
                self._cond.wait()
            self._writer = True
            self._writer_thread = threading.current_thread().ident

    def release_write(self):
        with self._cond:
            if not self._writer or self._writer_thread != threading.current_thread().ident:
                raise ValueError("release_write() called without holding the write lock")
            self._writer = False
            self._writer_thread = None
            self._cond.notify_all()
