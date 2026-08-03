import time
from collections import OrderedDict
from threading import RLock
from typing import Any, Hashable, Optional


class TTLCache:
    """A fixed-size cache whose entries expire after a configured TTL."""

    def __init__(self, ttl_seconds: float, max_size: int) -> None:
        self.ttl_seconds = ttl_seconds
        self.max_size = max_size
        self._entries: OrderedDict[Hashable, tuple[Any, float]] = OrderedDict()
        self._lock = RLock()

    def _remove_expired(self, now: float) -> None:
        expired_keys = [
            key
            for key, (_, expires_at) in self._entries.items()
            if now >= expires_at
        ]
        for key in expired_keys:
            self._entries.pop(key, None)

    def get(self, key: Hashable) -> Optional[Any]:
        if self.max_size <= 0:
            return None

        with self._lock:
            entry = self._entries.get(key)
            if entry is None:
                return None

            value, expires_at = entry
            if time.monotonic() >= expires_at:
                del self._entries[key]
                return None

            return value

    def set(self, key: Hashable, value: Any) -> None:
        if self.max_size <= 0:
            return

        with self._lock:
            now = time.monotonic()
            self._remove_expired(now)

            if key in self._entries:
                del self._entries[key]

            while len(self._entries) >= self.max_size:
                self._entries.popitem(last=False)

            self._entries[key] = (value, now + self.ttl_seconds)
