"""
A secure, self-contained implementation of a Peekable iterator wrapper.

This module provides the Peekable class, which wraps any iterable and
adds one-element look-ahead capability while remaining a valid iterator
itself (implements both __iter__ and __next__).
"""

from typing import Any, Iterable, Iterator, TypeVar

T = TypeVar("T")

# Sentinel object used internally to distinguish "no cached value" from
# a cached value that happens to be None or any other falsy/None-like value.
_SENTINEL = object()


class Peekable(Iterator[T]):
    """
    Wraps an iterable to provide one-element look-ahead functionality.

    Peekable is itself an iterator: it implements __iter__ (returning
    itself) and __next__ (advancing and returning the next item).

    Additional methods:
        peek(default=_SENTINEL): Return the next item without consuming
            it. If the underlying iterator is exhausted, raises
            StopIteration unless a default value was provided, in which
            case that default is returned instead.
        has_next() -> bool: Returns True if there is at least one more
            item available, False otherwise. Does not consume any items.

    Raises:
        TypeError: If the argument passed to the constructor is not
            iterable (i.e., iter(iterable) fails).
    """

    __slots__ = ("_iterator", "_cache")

    def __init__(self, iterable: Iterable[T]) -> None:
        # iter() will raise TypeError itself if iterable is not iterable;
        # we let that propagate naturally, which matches the required
        # behavior (raises TypeError if the argument is not iterable).
        try:
            self._iterator: Iterator[T] = iter(iterable)
        except TypeError as exc:
            # Re-raise as a clean TypeError without leaking internal
            # details about the original exception context.
            raise TypeError(
                f"Peekable requires an iterable, got {type(iterable).__name__!r}"
            ) from None

        # _cache holds a one-element look-ahead buffer. It is either
        # _SENTINEL (meaning "no cached value, need to pull from
        # underlying iterator") or a single-element tuple (value,)
        # holding the cached next value. Using a tuple wrapper lets us
        # cache values that are themselves None or falsy without
        # ambiguity.
        self._cache: Any = _SENTINEL

    def __iter__(self) -> "Peekable[T]":
        return self

    def __next__(self) -> T:
        if self._cache is not _SENTINEL:
            (value,) = self._cache
            self._cache = _SENTINEL
            return value
        # Let StopIteration propagate naturally from the underlying
        # iterator when exhausted.
        return next(self._iterator)

    def _fill_cache(self) -> bool:
        """
        Attempts to fill the internal cache from the underlying
        iterator if it is not already filled.

        Returns:
            True if a value is available in the cache after this call,
            False if the underlying iterator is exhausted.
        """
        if self._cache is not _SENTINEL:
            return True
        try:
            value = next(self._iterator)
        except StopIteration:
            return False
        self._cache = (value,)
        return True

    def peek(self, *default: Any) -> T:
        """
        Return the next item without consuming it.

        If called with no arguments and the iterator is exhausted,
        raises StopIteration. If called with one argument (a default
        value), returns that default instead of raising when exhausted.

        Calling peek() multiple times in a row without an intervening
        next() call returns the same item each time (idempotent).

        Raises:
            TypeError: If more than one positional argument is given.
        """
        if len(default) > 1:
            raise TypeError(
                f"peek expected at most 1 argument, got {len(default)}"
            )

        if self._fill_cache():
            (value,) = self._cache
            return value

        if default:
            return default[0]
        raise StopIteration

    def has_next(self) -> bool:
        """
        Return True if there is at least one more item available,
        without consuming it. Return False if the underlying iterator
        is exhausted.
        """
        return self._fill_cache()
