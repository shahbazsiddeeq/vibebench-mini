import time
import collections

class TTLCache:
    """
    A time-to-live (TTL) cache that stores key-value pairs.
    Entries expire after a specified TTL. When the cache is full,
    expired entries are reclaimed first, then the oldest remaining
    entry is evicted.
    """

    def __init__(self, ttl_seconds: float, max_size: int):
        """
        Initializes the TTLCache.

        Args:
            ttl_seconds: The time-to-live for cache entries in seconds.
                         Must be a non-negative number.
            max_size: The maximum number of entries the cache can hold.
                      Must be a non-negative integer. If 0, the cache holds nothing.
        """
        if not isinstance(ttl_seconds, (int, float)) or ttl_seconds < 0:
            raise ValueError("ttl_seconds must be a non-negative number.")
        if not isinstance(max_size, int) or max_size < 0:
            raise ValueError("max_size must be a non-negative integer.")

        self._ttl_seconds = ttl_seconds
        self._max_size = max_size
        # Stores (value, expiry_timestamp)
        self._cache = {}
        # Stores keys in order of insertion/update for eviction
        self._order = collections.deque()

    def _is_expired(self, key: str, current_time: float) -> bool:
        """
        Checks if a given key's entry has expired.

        Args:
            key: The key to check.
            current_time: The current timestamp to compare against.

        Returns:
            True if the entry is expired or not found, False otherwise.
        """
        if key not in self._cache:
            return True
        _, expiry_timestamp = self._cache[key]
        return current_time >= expiry_timestamp

    def _reclaim_expired(self, current_time: float):
        """
        Removes all expired entries from the cache.
        """
        # Iterate from the oldest entries in _order
        # Stop when a non-expired entry is found, as subsequent entries
        # are newer and thus also not expired (unless their TTL was shorter,
        # but all entries share the same _ttl_seconds).
        while self._order:
            key = self._order[0]
            if self._is_expired(key, current_time):
                self._order.popleft()
                del self._cache[key]
            else:
                break

    def get(self, key: str):
        """
        Retrieves the value associated with the given key.

        Args:
            key: The key to retrieve.

        Returns:
            The value if the key exists and has not expired, otherwise None.
        """
        if not isinstance(key, str):
            # For security and consistency, only allow string keys.
            # Other types could lead to unexpected behavior or hash collisions.
            return None

        if self._max_size == 0:
            return None

        current_time = time.monotonic()
        self._reclaim_expired(current_time)

        if key in self._cache:
            value, expiry_timestamp = self._cache[key]
            # Re-check expiry after reclamation, just in case
            if current_time < expiry_timestamp:
                return value
            else:
                # Should have been reclaimed, but handle defensively
                del self._cache[key]
                # Remove from order if it's still there (edge case)
                try:
                    self._order.remove(key)
                except ValueError:
                    pass # Already removed or not in order
        return None

    def set(self, key: str, value):
        """
        Stores or updates a key-value pair in the cache.
        The entry will expire after `ttl_seconds`.

        Args:
            key: The key to store. Must be a string.
            value: The value to associate with the key.
        """
        if not isinstance(key, str):
            raise ValueError("Key must be a string.")

        if self._max_size == 0:
            return

        current_time = time.monotonic()
        self._reclaim_expired(current_time)

        if key in self._cache:
            # Update existing entry
            # Remove old entry from order to re-add at the end (most recently used/set)
            try:
                self._order.remove(key)
            except ValueError:
                # Key might have been removed by _reclaim_expired but still in _cache
                # if _reclaim_expired was called before this set operation.
                pass
        else:
            # New entry, check if eviction is needed
            if len(self._cache) >= self._max_size:
                # Evict oldest non-expired entry
                while self._order:
                    oldest_key = self._order.popleft()
                    if oldest_key in self._cache: # Ensure it wasn't removed by _reclaim_expired
                        del self._cache[oldest_key]
                        break
                    # If oldest_key was already removed, continue to next oldest
                else:
                    # This case should ideally not be reached if _reclaim_expired
                    # and the eviction logic are working correctly, but as a fallback
                    # if cache is full and _order is empty (e.g., all items expired
                    # but not yet fully processed by _reclaim_expired in a specific sequence),
                    # we might need to just drop the new item or raise an error.
                    # For this problem, we assume _order and _cache stay in sync
                    # for live items. If _order is empty here, it implies _cache is also empty
                    # or only contains expired items that _reclaim_expired should have handled.
                    # If _cache is still full but _order is empty, it's an inconsistency.
                    # For now, we'll assume _reclaim_expired handles it.
                    # If _cache is still full and _order is empty, it means all items
                    # in _cache are expired but _reclaim_expired failed to remove them from _order.
                    # This is an internal inconsistency.
                    # For robustness, if _cache is still full here, we could just return.
                    if len(self._cache) >= self._max_size:
                        return # Cannot add, cache is full and no space could be made.

        # Add/update the entry
        expiry_timestamp = current_time + self._ttl_seconds
        self._cache[key] = (value, expiry_timestamp)
        self._order.append(key)
