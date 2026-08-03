"""
src/solution.py

A thread-safe Token Bucket rate limiter.

Design notes (security-conscious):
- All public inputs are validated with clear, generic error messages
  (no internal state or stack traces are leaked).
- Uses threading.Lock for atomic check-and-consume semantics.
- No use of eval/exec, no external I/O, no randomness needed here
  (kept for completeness per instructions: not applicable to this module).
"""

import threading


class TokenBucket:
    """A simple thread-safe token bucket rate limiter.

    Args:
        capacity: Maximum number of tokens the bucket can hold. Must be
            an integer or float >= 1, otherwise ValueError is raised.

    The bucket starts full (tokens == capacity).
    """

    __slots__ = ("_capacity", "_tokens", "_lock")

    def __init__(self, capacity):
        if isinstance(capacity, bool) or not isinstance(capacity, (int, float)):
            raise ValueError("capacity must be a number")
        if capacity < 1:
            raise ValueError("capacity must be >= 1")

        self._capacity = capacity
        self._tokens = capacity
        self._lock = threading.Lock()

    @property
    def tokens(self):
        """Current number of available tokens (read-only)."""
        with self._lock:
            return self._tokens

    def allow(self, n=1):
        """Attempt to atomically consume `n` tokens.

        Returns True and consumes `n` tokens if at least `n` tokens are
        available. Otherwise returns False and consumes nothing.
        """
        if isinstance(n, bool) or not isinstance(n, (int, float)):
            raise ValueError("n must be a number")
        if n < 0:
            raise ValueError("n must be non-negative")

        with self._lock:
            if self._tokens >= n:
                self._tokens -= n
                return True
            return False

    def refill(self, n):
        """Add `n` tokens to the bucket, capped at capacity."""
        if isinstance(n, bool) or not isinstance(n, (int, float)):
            raise ValueError("n must be a number")
        if n < 0:
            raise ValueError("n must be non-negative")

        with self._lock:
            self._tokens = min(self._capacity, self._tokens + n)
