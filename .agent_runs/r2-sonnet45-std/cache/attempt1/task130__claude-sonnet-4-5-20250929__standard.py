import threading


class RWLock:
    def __init__(self):
        self._readers = 0
        self._writers = 0
        self._read_ready = threading.Condition(threading.Lock())
        self._reader_threads = {}  # Track which threads hold read locks
        self._writer_thread = None  # Track which thread holds write lock
        
    @property
    def active_readers(self):
        with self._read_ready:
            return self._readers
    
    def acquire_read(self):
        thread_id = threading.get_ident()
        with self._read_ready:
            # Wait while there's a writer
            while self._writers > 0:
                self._read_ready.wait()
            
            # Increment reader count
            self._readers += 1
            # Track this thread as a reader
            self._reader_threads[thread_id] = self._reader_threads.get(thread_id, 0) + 1
    
    def release_read(self):
        thread_id = threading.get_ident()
        with self._read_ready:
            # Check if this thread holds a read lock
            if thread_id not in self._reader_threads or self._reader_threads[thread_id] == 0:
                raise ValueError("Cannot release read lock that is not held")
            
            # Decrement reader count
            self._readers -= 1
            self._reader_threads[thread_id] -= 1
            
            # Clean up tracking if no more read locks for this thread
            if self._reader_threads[thread_id] == 0:
                del self._reader_threads[thread_id]
            
            # Notify waiting writers if no more readers
            if self._readers == 0:
                self._read_ready.notify_all()
    
    def acquire_write(self):
        thread_id = threading.get_ident()
        with self._read_ready:
            # Wait while there are readers or another writer
            while self._readers > 0 or self._writers > 0:
                self._read_ready.wait()
            
            # Acquire write lock
            self._writers = 1
            self._writer_thread = thread_id
    
    def release_write(self):
        thread_id = threading.get_ident()
        with self._read_ready:
            # Check if this thread holds the write lock
            if self._writer_thread != thread_id or self._writers == 0:
                raise ValueError("Cannot release write lock that is not held")
            
            # Release write lock
            self._writers = 0
            self._writer_thread = None
            
            # Notify all waiting threads (readers and writers)
            self._read_ready.notify_all()
