import threading

class TokenBucket:
    """
    Implements a thread-safe Token Bucket algorithm for rate limiting.

    The bucket starts full. Tokens can be consumed atomically, and the bucket
    can be refilled, capped at its capacity.
    """

    def __init__(self, capacity: int):
        """
        Initializes a new TokenBucket.

        Args:
            capacity: The maximum number of tokens the bucket can hold.
                      Must be an integer greater than or equal to 1.

        Raises:
            ValueError: If capacity is less than 1.
            TypeError: If capacity is not an integer.
        """
        if not isinstance(capacity, int):
            raise TypeError("Capacity must be an integer.")
        if capacity < 1:
            raise ValueError("Capacity must be at least 1.")

        self._capacity = capacity
        self._tokens = capacity  # Bucket starts full
        self._lock = threading.Lock()

    @property
    def tokens(self) -> int:
        """
        Returns the current number of tokens in the bucket.
        This property is read-only.
        """
        with self._lock:
            return self._tokens

    def allow(self, n: int = 1) -> bool:
        """
        Attempts to consume 'n' tokens from the bucket.

        This operation is atomic: if 'n' tokens are available, they are
        consumed and True is returned. Otherwise, no tokens are consumed
        and False is returned.

        Args:
            n: The number of tokens to consume. Must be an integer greater
               than or equal to 1. Defaults to 1.

        Returns:
            True if 'n' tokens were successfully consumed, False otherwise.

        Raises:
            ValueError: If n is less than 1.
            TypeError: If n is not an integer.
        """
        if not isinstance(n, int):
            raise TypeError("Number of tokens 'n' must be an integer.")
        if n < 1:
            raise ValueError("Number of tokens 'n' must be at least 1.")

        with self._lock:
            if self._tokens >= n:
                self._tokens -= n
                return True
            return False

    def refill(self, n: int) -> None:
        """
        Adds 'n' tokens to the bucket, up to its capacity.

        Args:
            n: The number of tokens to add. Must be an integer greater
               than or equal to 0.

        Raises:
            ValueError: If n is less than 0.
            TypeError: If n is not an integer.
        """
        if not isinstance(n, int):
            raise TypeError("Number of tokens 'n' to refill must be an integer.")
        if n < 0:
            raise ValueError("Number of tokens 'n' to refill cannot be negative.")

        with self._lock:
            self._tokens = min(self._capacity, self._tokens + n)
