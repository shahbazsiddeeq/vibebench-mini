class Peekable:
    """A wrapper that adds one-element look-ahead to any iterable."""
    
    def __init__(self, iterable):
        """Initialize Peekable with an iterable.
        
        Args:
            iterable: Any iterable object
            
        Raises:
            TypeError: If the argument is not iterable
        """
        try:
            self._iterator = iter(iterable)
        except TypeError:
            raise TypeError(f"'{type(iterable).__name__}' object is not iterable")
        
        self._peeked = None
        self._has_peeked = False
    
    def __iter__(self):
        """Return self as the iterator."""
        return self
    
    def __next__(self):
        """Return the next item, advancing the iterator.
        
        Raises:
            StopIteration: When the iterator is exhausted
        """
        if self._has_peeked:
            self._has_peeked = False
            return self._peeked
        return next(self._iterator)
    
    def peek(self, default=None):
        """Look ahead at the next item without consuming it.
        
        Args:
            default: Optional default value to return if exhausted.
                     If not provided, raises StopIteration when exhausted.
        
        Returns:
            The next item without consuming it, or default if exhausted and provided.
            
        Raises:
            StopIteration: If exhausted and no default is provided
        """
        if not self._has_peeked:
            try:
                self._peeked = next(self._iterator)
                self._has_peeked = True
            except StopIteration:
                if default is None:
                    # Check if default was actually provided
                    # We need to distinguish between peek() and peek(None)
                    raise
                return default
        return self._peeked
    
    def peek(self, *args):
        """Look ahead at the next item without consuming it.
        
        Args:
            *args: Optional default value. If provided, returns it when exhausted.
                   If not provided, raises StopIteration when exhausted.
        
        Returns:
            The next item without consuming it, or default if exhausted and provided.
            
        Raises:
            StopIteration: If exhausted and no default is provided
        """
        if len(args) > 1:
            raise TypeError(f"peek() takes at most 1 argument ({len(args)} given)")
        
        if not self._has_peeked:
            try:
                self._peeked = next(self._iterator)
                self._has_peeked = True
            except StopIteration:
                if len(args) == 0:
                    raise
                return args[0]
        return self._peeked
    
    def has_next(self):
        """Check if at least one more item is available.
        
        Returns:
            True if at least one more item is available, False otherwise
        """
        if self._has_peeked:
            return True
        try:
            self._peeked = next(self._iterator)
            self._has_peeked = True
            return True
        except StopIteration:
            return False
