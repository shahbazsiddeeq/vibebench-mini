from typing import Iterable, Iterator, List
import itertools

def chunked(iterable: Iterable, size: int) -> Iterator[List]:
    if size < 1:
        raise ValueError("Size must be at least 1")

    iterator = iter(iterable)
    while True:
        chunk = list(itertools.islice(iterator, size))
        if not chunk:
            break
        yield chunk
