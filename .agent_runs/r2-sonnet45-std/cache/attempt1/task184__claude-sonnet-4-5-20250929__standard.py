class Peekable:
    """A wrapper that adds one-element look-ahead to any iterable."""
    
    _SENTINEL = object()
    
    def __init__(self, iterable):
        """Initialize with any iterable. Raises TypeError if not iterable."""
        try:
            self._iterator = iter(iterable)
        except TypeError:
            raise TypeError(f"'{type(iterable).__name__}' object is not iterable")
        
        self._peeked = self._SENTINEL
    
    def __iter__(self):
        """Return self as this is its own iterator."""
        return self
    
    def __next__(self):
        """Return the next item, advancing the iterator."""
        if self._peeked is not self._SENTINEL:
            # We have a peeked value, return it and clear the cache
            value = self._peeked
            self._peeked = self._SENTINEL
            return value
        else:
            # No peeked value, get next from underlying iterator
            return next(self._iterator)
    
    def peek(self, *args):
        """
        Return the next item WITHOUT consuming it.
        
        If called without arguments, raises StopIteration when exhausted.
        If called with one argument (default), returns that default when exhausted.
        """
        if len(args) > 1:
            raise TypeError(f"peek() takes at most 1 argument ({len(args)} given)")
        
        has_default = len(args) == 1
        
        if self._peeked is not self._SENTINEL:
            # Already peeked, return cached value
            return self._peeked
        
        try:
            # Try to get next value and cache it
            self._peeked = next(self._iterator)
            return self._peeked
        except StopIteration:
            if has_default:
                return args[0]
            else:
                raise
    
    def has_next(self):
        """Return True if at least one more item is available, False otherwise."""
        try:
            self.peek()
            return True
        except StopIteration:
            return False
