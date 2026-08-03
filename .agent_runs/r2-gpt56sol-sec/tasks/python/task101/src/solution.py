"""Thread-safe singleton implementation."""

from __future__ import annotations

import threading
from typing import ClassVar, Optional


class Singleton:
    """A class with at most one cached instance until reset."""

    _instance: ClassVar[Optional["Singleton"]] = None
    _lock: ClassVar[threading.RLock] = threading.RLock()

    def __new__(cls) -> "Singleton":
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
            return cls._instance

    @classmethod
    def reset(cls) -> None:
        """Discard the cached instance."""
        with cls._lock:
            cls._instance = None
