import time
from collections import OrderedDict
from typing import Any, Optional


class TTLCache:
    """
    A simple TTL (time-to-live) cache with a maximum size.

    Entries expire `ttl_seconds` after they are set. When the cache is at
    capacity, expired entries are reclaimed first before evicting the
    oldest remaining entry.
    """

    def __init__(self, ttl_seconds: float, max_size: int) -> None:
        if not isinstance(ttl_seconds, (int, float)) or isinstance(ttl_seconds, bool):
            raise TypeError("ttl_seconds must be a real number")
        if ttl_seconds <= 0:
            raise ValueError("ttl_seconds must be positive")
        if not isinstance(max_size, int) or isinstance(max_size, bool):
            raise TypeError("max_size must be an integer")

        self._ttl = float(ttl_seconds)
        self._max_size = max_size
        # key -> (value, expiry_timestamp)
        self._store: "OrderedDict[Any, tuple]" = OrderedDict()

    def _now(self) -> float:
        return time.monotonic()

    def _is_expired(self, expiry: float, now: Optional[float] = None) -> bool:
        if now is None:
            now = self._now()
        return now >= expiry

    def _purge_expired(self) -> None:
        """Remove all expired entries from the cache."""
        now = self._now()
        expired_keys = [
            key for key, (_, expiry) in self._store.items()
            if self._is_expired(expiry, now)
        ]
        for key in expired_keys:
            del self._store[key]

    def get(self, key: Any) -> Optional[Any]:
        """
        Return the value for `key`, or None if missing or expired.
        Expired entries are removed lazily on access.
        """
        entry = self._store.get(key)
        if entry is None:
            return None

        value, expiry = entry
        if self._is_expired(expiry):
            # Lazily remove expired entry.
            del self._store[key]
            return None

        return value

    def set(self, key: Any, value: Any) -> None:
        """
        Store or update `key` with `value`. No-op if max_size <= 0.
        Evicts expired entries first, then the oldest remaining entry,
        when the cache is full.
        """
        if self._max_size <= 0:
            return

        now = self._now()
        expiry = now + self._ttl

        if key in self._store:
            # Update existing key: refresh value, expiry, and order.
            self._store[key] = (value, expiry)
            self._store.move_to_end(key)
            return

        # Make room if necessary.
        if len(self._store) >= self._max_size:
            self._purge_expired()

        if len(self._store) >= self._max_size:
            # Still full after purging expired: evict oldest remaining entry.
            if self._store:
                oldest_key = next(iter(self._store))
                del self._store[oldest_key]

        self._store[key] = (value, expiry)
        self._store.move_to_end(key)
