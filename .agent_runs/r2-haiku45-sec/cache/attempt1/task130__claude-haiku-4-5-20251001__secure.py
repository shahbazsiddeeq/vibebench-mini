import threading
from typing import Optional


class RWLock:
    """A read-write lock that allows multiple concurrent readers but exclusive writer access."""
    
    def __init__(self) -> None:
        """Initialize the read-write lock."""
        self._readers = 0
        self._writers = 0
        self._read_ready = threading.Condition(threading.RLock())
        self._write_ready = threading.Condition(threading.RLock())
        self._read_waiters = 0
        self._write_waiters = 0
    
    @property
    def active_readers(self) -> int:
        """Return the current number of active readers."""
        with self._read_ready:
            return self._readers
    
    def acquire_read(self) -> None:
        """Acquire a read lock. Multiple readers can hold simultaneously."""
        self._read_ready.acquire()
        try:
            # Wait while there are active writers or waiting writers
            while self._writers > 0 or self._write_waiters > 0:
                self._read_ready.wait()
            self._readers += 1
        finally:
            self._read_ready.release()
    
    def release_read(self) -> None:
        """Release a read lock. Raises ValueError if no read lock is held."""
        self._read_ready.acquire()
        try:
            if self._readers <= 0:
                raise ValueError("release_read() called without holding a read lock")
            self._readers -= 1
            if self._readers == 0:
                self._read_ready.notify_all()
        finally:
            self._read_ready.release()
    
    def acquire_write(self) -> None:
        """Acquire a write lock. Exclusive access - blocks readers and other writers."""
        self._read_ready.acquire()
        try:
            self._write_waiters += 1
            try:
                # Wait while there are active readers or active writers
                while self._readers > 0 or self._writers > 0:
                    self._read_ready.wait()
                self._writers += 1
            finally:
                self._write_waiters -= 1
        finally:
            self._read_ready.release()
    
    def release_write(self) -> None:
        """Release a write lock. Raises ValueError if no write lock is held."""
        self._read_ready.acquire()
        try:
            if self._writers <= 0:
                raise ValueError("release_write() called without holding a write lock")
            self._writers -= 1
            self._read_ready.notify_all()
        finally:
            self._read_ready.release()
