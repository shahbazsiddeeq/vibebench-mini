import threading


class RWLock:
    """
    A read-write lock that allows multiple concurrent readers or a single writer.
    
    - Multiple readers can hold the lock simultaneously
    - Only one writer can hold the lock at a time
    - Writers have exclusive access (no readers or other writers)
    - Readers block while a writer holds the lock
    - Writers block while any readers or another writer holds the lock
    """
    
    def __init__(self):
        self._lock = threading.Lock()
        self._readers = 0
        self._writers = 0
        self._read_ready = threading.Condition(self._lock)
        self._write_ready = threading.Condition(self._lock)
        # Track which thread holds write lock for validation
        self._write_owner = None
        # Track reader counts per thread for validation
        self._reader_counts = {}
    
    def acquire_read(self):
        """Acquire a read lock. Blocks if a writer holds the lock."""
        current_thread = threading.current_thread()
        
        with self._lock:
            # Wait while there's an active writer
            while self._writers > 0:
                self._read_ready.wait()
            
            self._readers += 1
            # Track this thread's reader count
            self._reader_counts[current_thread] = self._reader_counts.get(current_thread, 0) + 1
    
    def release_read(self):
        """Release a read lock. Raises ValueError if not held."""
        current_thread = threading.current_thread()
        
        with self._lock:
            # Validate that this thread holds a read lock
            if current_thread not in self._reader_counts or self._reader_counts[current_thread] <= 0:
                raise ValueError("release_read() called without holding a read lock")
            
            self._readers -= 1
            self._reader_counts[current_thread] -= 1
            
            # Clean up if this thread has no more read locks
            if self._reader_counts[current_thread] == 0:
                del self._reader_counts[current_thread]
            
            # If no more readers, notify waiting writers
            if self._readers == 0:
                self._write_ready.notify()
    
    def acquire_write(self):
        """Acquire a write lock. Blocks if any readers or another writer holds the lock."""
        current_thread = threading.current_thread()
        
        with self._lock:
            # Wait while there are active readers or another writer
            while self._readers > 0 or self._writers > 0:
                self._write_ready.wait()
            
            self._writers = 1
            self._write_owner = current_thread
    
    def release_write(self):
        """Release a write lock. Raises ValueError if not held."""
        current_thread = threading.current_thread()
        
        with self._lock:
            # Validate that this thread holds the write lock
            if self._writers == 0 or self._write_owner != current_thread:
                raise ValueError("release_write() called without holding a write lock")
            
            self._writers = 0
            self._write_owner = None
            
            # Notify all waiting readers and writers
            self._read_ready.notify_all()
            self._write_ready.notify()
    
    @property
    def active_readers(self):
        """Return the current number of active readers."""
        with self._lock:
            return self._readers
