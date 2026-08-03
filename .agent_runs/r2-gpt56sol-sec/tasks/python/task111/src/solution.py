from collections.abc import Iterable, Iterator
from itertools import islice
from typing import TypeVar

T = TypeVar("T")


def chunked(iterable: Iterable[T], size: int) -> Iterator[list[T]]:
    """Yield successive lists containing up to ``size`` items."""
    if not isinstance(size, int) or isinstance(size, bool) or size < 1:
        raise ValueError("size must be a positive integer")

    iterator = iter(iterable)
    while chunk := list(islice(iterator, size)):
        yield chunk
