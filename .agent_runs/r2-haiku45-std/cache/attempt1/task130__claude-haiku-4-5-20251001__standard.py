import threading


class RWLock:
    """A read-write lock that allows multiple concurrent readers but exclusive writer access."""
    
    def __init__(self):
        self._readers = 0
        self._writers = 0
        self._read_ready = threading.Condition(threading.RLock())
        self._write_lock = threading.Lock()
        self._writer_thread = None
    
    def acquire_read(self):
        """Acquire a read lock. Multiple readers can hold this simultaneously."""
        self._read_ready.acquire()
        try:
            # Wait while there are writers or a writer is waiting
            while self._writers > 0:
                self._read_ready.wait()
            self._readers += 1
        finally:
            self._read_ready.release()
    
    def release_read(self):
        """Release a read lock."""
        self._read_ready.acquire()
        try:
            if self._readers <= 0:
                raise ValueError("release_read() called without a matching acquire_read()")
            self._readers -= 1
            if self._readers == 0:
                self._read_ready.notifyAll()
        finally:
            self._read_ready.release()
    
    def acquire_write(self):
        """Acquire a write lock. Only one writer can hold this at a time."""
        self._write_lock.acquire()
        self._read_ready.acquire()
        try:
            self._writers += 1
            # Wait for all readers to finish
            while self._readers > 0:
                self._read_ready.wait()
        finally:
            self._read_ready.release()
        self._writer_thread = threading.current_thread()
    
    def release_write(self):
        """Release a write lock."""
        if self._writer_thread != threading.current_thread():
            raise ValueError("release_write() called without a matching acquire_write()")
        
        self._read_ready.acquire()
        try:
            self._writers -= 1
            self._read_ready.notifyAll()
        finally:
            self._read_ready.release()
        
        self._writer_thread = None
        self._write_lock.release()
    
    @property
    def active_readers(self):
        """Return the current number of active readers."""
        self._read_ready.acquire()
        try:
            return self._readers
        finally:
            self._read_ready.release()
