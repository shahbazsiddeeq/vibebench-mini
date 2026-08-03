from itertools import islice
from typing import Iterable, Iterator, List, TypeVar

T = TypeVar("T")


def chunked(iterable: Iterable[T], size: int) -> Iterator[List[T]]:
    """Yield successive lists containing up to ``size`` elements."""
    if size < 1:
        raise ValueError("size must be at least 1")

    iterator = iter(iterable)
    while chunk := list(islice(iterator, size)):
        yield chunk
