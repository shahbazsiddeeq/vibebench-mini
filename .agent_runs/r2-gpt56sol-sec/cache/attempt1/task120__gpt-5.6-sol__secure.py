"""Thread-safe time-to-live cache implementation."""

from __future__ import annotations

import math
import time
from collections import OrderedDict
from numbers import Integral, Real
from threading import RLock
from typing import Any


class TTLCache:
    """A fixed-size cache whose entries expire after a shared TTL."""

    def __init__(self, ttl_seconds: Real, max_size: Integral) -> None:
        if isinstance(ttl_seconds, bool) or not isinstance(ttl_seconds, Real):
            raise TypeError("ttl_seconds must be a real number")
        if math.isnan(float(ttl_seconds)):
            raise ValueError("ttl_seconds must not be NaN")
        if isinstance(max_size, bool) or not isinstance(max_size, Integral):
            raise TypeError("max_size must be an integer")

        self._ttl = ttl_seconds
        self._max_size = int(max_size)
        self._entries: OrderedDict[Any, tuple[float, Any]] = OrderedDict()
        self._lock = RLock()

    def _purge_expired(self, now: float) -> None:
        expired_keys = [
            key
            for key, (set_at, _) in self._entries.items()
            if now - set_at >= self._ttl
        ]
        for key in expired_keys:
            self._entries.pop(key, None)

    def get(self, key: Any) -> Any:
        """Return the cached value, or None if missing or expired."""
        if self._max_size <= 0:
            return None

        now = time.monotonic()
        with self._lock:
            entry = self._entries.get(key)
            if entry is None:
                return None

            set_at, value = entry
            if now - set_at >= self._ttl:
                self._entries.pop(key, None)
                return None
            return value

    def set(self, key: Any, value: Any) -> None:
        """Store or update a value and reset its expiration time."""
        if self._max_size <= 0 or self._ttl <= 0:
            return

        now = time.monotonic()
        with self._lock:
            self._purge_expired(now)

            if key in self._entries:
                del self._entries[key]

            while len(self._entries) >= self._max_size:
                self._entries.popitem(last=False)

            self._entries[key] = (now, value)
