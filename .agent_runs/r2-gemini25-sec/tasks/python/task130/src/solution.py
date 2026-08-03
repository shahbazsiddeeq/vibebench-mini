import threading

class RWLock:
    """
    A Read-Write lock implementation allowing multiple concurrent readers
    or a single exclusive writer.
    """

    def __init__(self):
        self._read_ready = threading.Condition(threading.Lock())
        self._readers = 0
        self._writer_active = False
        self._writer_waiting = 0

    @property
    def active_readers(self) -> int:
        """
        Reports the current number of active readers holding the lock.
        """
        with self._read_ready:
            return self._readers

    def acquire_read(self) -> None:
        """
        Acquires a read lock. Multiple readers can hold the lock concurrently.
        Blocks if a writer currently holds or is waiting for the lock.
        """
        with self._read_ready:
            while self._writer_active or self._writer_waiting > 0:
                self._read_ready.wait()
            self._readers += 1

    def release_read(self) -> None:
        """
        Releases a read lock.
        Raises ValueError if no read lock is currently held by any reader.
        """
        with self._read_ready:
            if self._readers == 0:
                raise ValueError("Cannot release read lock: no reader currently holds it.")
            self._readers -= 1
            if self._readers == 0:
                # If no readers are left, notify any waiting writers
                self._read_ready.notify_all()

    def acquire_write(self) -> None:
        """
        Acquires a write lock. Only one writer can hold the lock at a time,
        and no readers can hold it concurrently.
        Blocks if any reader or another writer currently holds the lock.
        """
        with self._read_ready:
            self._writer_waiting += 1
            while self._readers > 0 or self._writer_active:
                self._read_ready.wait()
            self._writer_active = True
            self._writer_waiting -= 1

    def release_write(self) -> None:
        """
        Releases a write lock.
        Raises ValueError if no write lock is currently held by the writer.
        """
        with self._read_ready:
            if not self._writer_active:
                raise ValueError("Cannot release write lock: no writer currently holds it.")
            self._writer_active = False
            # Notify all waiting readers and writers
            self._read_ready.notify_all()
