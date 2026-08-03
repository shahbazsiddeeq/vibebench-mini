import collections

class LRUCache:
    """
    A Least Recently Used (LRU) cache implementation.

    This cache evicts the least recently used item when it reaches its capacity.
    It supports O(1) average time complexity for get and put operations.
    """

    def __init__(self, capacity: int):
        """
        Initializes the LRU cache with a given capacity.

        Args:
            capacity: The maximum number of key-value pairs the cache can hold.

        Raises:
            ValueError: If the capacity is less than 1.
        """
        if not isinstance(capacity, int) or capacity < 1:
            raise ValueError("Capacity must be a positive integer.")

        self._capacity = capacity
        # Using an OrderedDict to maintain insertion order, which effectively
        # serves as a recency list. The most recently used items are at the end.
        self._cache = collections.OrderedDict()

    def get(self, key: int) -> int:
        """
        Retrieves the value associated with the given key.

        If the key exists, its access updates its recency, making it the
        most recently used item.

        Args:
            key: The key to retrieve.

        Returns:
            The value associated with the key, or -1 if the key is not found.
        """
        # Input validation for key type (assuming keys are integers based on tests)
        if not isinstance(key, int):
            # For security and robustness, we could log this or raise a more specific error
            # but for this problem, returning -1 for non-integer keys is a safe default
            # as it implies "not found" without exposing internal structure.
            return -1

        if key not in self._cache:
            return -1

        # Move the accessed item to the end to mark it as most recently used
        value = self._cache.pop(key)
        self._cache[key] = value
        return value

    def put(self, key: int, value: int) -> None:
        """
        Inserts or updates a key-value pair in the cache.

        If the key already exists, its value is updated, and its recency is
        refreshed. If the cache is full and a new key is inserted, the
        least recently used item is evicted.

        Args:
            key: The key to insert or update.
            value: The value to associate with the key.
        """
        # Input validation for key and value types (assuming integers based on tests)
        if not isinstance(key, int) or not isinstance(value, int):
            # Silently ignore invalid types or raise an error depending on requirements.
            # For a cache, silently ignoring might be acceptable to prevent crashes,
            # but raising an error is generally safer for input validation.
            # Given the problem context, we'll assume valid types are passed or
            # handle them gracefully without crashing.
            return

        if key in self._cache:
            # Update existing key: remove and re-add to update recency
            self._cache.pop(key)
        elif len(self._cache) >= self._capacity:
            # Cache is full, evict the least recently used item (first item)
            self._cache.popitem(last=False)

        self._cache[key] = value
