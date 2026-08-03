class Peekable:
    """A wrapper that adds one-element look-ahead to any iterable."""
    
    def __init__(self, iterable):
        """Initialize with an iterable.
        
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
        """Return the next item and advance the iterator.
        
        Returns:
            The next item from the iterator
            
        Raises:
            StopIteration: When the iterator is exhausted
        """
        if self._has_peeked:
            # Return the peeked value and clear the peek cache
            value = self._peeked
            self._peeked = None
            self._has_peeked = False
            return value
        else:
            # Get the next value from the underlying iterator
            return next(self._iterator)
    
    def peek(self, *args):
        """Return the next item without consuming it.
        
        Args:
            *args: Optional default value to return if exhausted
            
        Returns:
            The next item that would be returned by __next__,
            or the default value if provided and iterator is exhausted
            
        Raises:
            StopIteration: When exhausted and no default is provided
        """
        if len(args) > 1:
            raise TypeError(f"peek() takes at most 1 argument ({len(args)} given)")
        
        if not self._has_peeked:
            # Try to get the next value and cache it
            try:
                self._peeked = next(self._iterator)
                self._has_peeked = True
            except StopIteration:
                if args:
                    return args[0]
                raise
        
        return self._peeked
    
    def has_next(self):
        """Check if at least one more item is available.
        
        Returns:
            bool: True if at least one item is available, False otherwise
        """
        try:
            self.peek()
            return True
        except StopIteration:
            return False
