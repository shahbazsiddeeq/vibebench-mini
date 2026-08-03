class Peekable:
    """
    A wrapper that adds one-element look-ahead to an iterator.

    The constructor accepts any iterable and raises TypeError if the argument
    is not iterable.

    It implements the iterator protocol (__iter__ and __next__).
    """

    def __init__(self, iterable):
        """
        Initializes the Peekable iterator.

        Args:
            iterable: Any iterable object.

        Raises:
            TypeError: If the provided argument is not iterable.
        """
        try:
            self._iterator = iter(iterable)
        except TypeError as e:
            raise TypeError(f"'{type(iterable).__name__}' object is not iterable") from e
        self._peeked_item = None
        self._has_peeked = False

    def __iter__(self):
        """
        Returns the iterator itself, making it its own iterator.
        """
        return self

    def __next__(self):
        """
        Returns the next item, advancing the underlying iterator.

        Raises:
            StopIteration: When exhausted.
        """
        if self._has_peeked:
            item = self._peeked_item
            self._peeked_item = None
            self._has_peeked = False
            return item
        else:
            return next(self._iterator)

    def peek(self, default=None):
        """
        Returns the next item WITHOUT consuming it.

        If called with no arguments, raises StopIteration if there are no more items.
        If called with one argument (default), returns default (rather than raising)
        when exhausted.

        Args:
            default: An optional default value to return if the iterator is exhausted.

        Returns:
            The next item or the default value if provided and exhausted.

        Raises:
            StopIteration: If no default is provided and the iterator is exhausted.
        """
        if not self._has_peeked:
            try:
                self._peeked_item = next(self._iterator)
                self._has_peeked = True
            except StopIteration:
                if default is not None:
                    return default
                raise

        return self._peeked_item

    def has_next(self) -> bool:
        """
        Returns True if at least one more item is available and False otherwise,
        without consuming anything.
        """
        if self._has_peeked:
            return True
        try:
            self.peek()
            return True
        except StopIteration:
            return False
