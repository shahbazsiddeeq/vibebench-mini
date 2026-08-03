import time
import collections

class TTLCache:
    def __init__(self, ttl_seconds, max_size):
        self.ttl_seconds = ttl_seconds
        self.max_size = max_size
        self.cache = collections.OrderedDict() # Stores (key, (value, expiry_time))

    def _is_expired(self, expiry_time):
        return time.monotonic() >= expiry_time

    def _reclaim_expired(self):
        # Iterate from the oldest to reclaim expired entries
        keys_to_remove = []
        for key, (value, expiry_time) in self.cache.items():
            if self._is_expired(expiry_time):
                keys_to_remove.append(key)
            else:
                # Since OrderedDict maintains insertion order,
                # if an entry is not expired, subsequent entries are also not expired
                break
        
        for key in keys_to_remove:
            del self.cache[key]

    def get(self, key):
        if self.max_size <= 0:
            return None

        if key not in self.cache:
            return None

        value, expiry_time = self.cache[key]

        if self._is_expired(expiry_time):
            del self.cache[key]
            return None
        
        # Move the accessed item to the end to mark it as recently used (for LRU if needed, though not strictly LRU here)
        # This is important for maintaining order for eviction if not expired
        self.cache.move_to_end(key)
        return value

    def set(self, key, value):
        if self.max_size <= 0:
            return

        current_time = time.monotonic()
        expiry_time = current_time + self.ttl_seconds

        if key in self.cache:
            # Update existing entry and move to end
            self.cache[key] = (value, expiry_time)
            self.cache.move_to_end(key)
            return

        # Key is new, need to make space if cache is full
        if len(self.cache) >= self.max_size:
            # First, try to reclaim expired entries
            self._reclaim_expired()

            # If still full after reclaiming, evict the oldest non-expired entry
            if len(self.cache) >= self.max_size:
                # The first item in OrderedDict is the oldest
                # Since _reclaim_expired already removed expired ones from the front,
                # the first remaining item must be the oldest non-expired one.
                oldest_key = next(iter(self.cache))
                del self.cache[oldest_key]
        
        # Add the new entry
        self.cache[key] = (value, expiry_time)
