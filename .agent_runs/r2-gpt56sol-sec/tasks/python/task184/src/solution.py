"""A one-item look-ahead iterator wrapper."""

_MISSING = object()
_EMPTY = object()


class Peekable:
    """Wrap an iterable and provide non-consuming one-item look-ahead."""

    __slots__ = ("_iterator", "_buffer", "_exhausted")

    def __init__(self, iterable):
        try:
            self._iterator = iter(iterable)
        except TypeError:
            raise TypeError("Peekable requires an iterable") from None

        self._buffer = _EMPTY
        self._exhausted = False

    def __iter__(self):
        return self

    def __next__(self):
        if self._buffer is not _EMPTY:
            item = self._buffer
            self._buffer = _EMPTY
            return item

        if self._exhausted:
            raise StopIteration

        try:
            return next(self._iterator)
        except StopIteration:
            self._exhausted = True
            raise

    def _fill_buffer(self):
        if self._buffer is not _EMPTY or self._exhausted:
            return

        try:
            self._buffer = next(self._iterator)
        except StopIteration:
            self._exhausted = True

    def peek(self, default=_MISSING):
        """Return the next item without consuming it."""
        self._fill_buffer()

        if self._buffer is not _EMPTY:
            return self._buffer

        if default is not _MISSING:
            return default

        raise StopIteration

    def has_next(self):
        """Return whether another item is available without consuming it."""
        self._fill_buffer()
        return self._buffer is not _EMPTY
