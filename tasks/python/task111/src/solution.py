from typing import Iterable, Iterator


def chunked(iterable: Iterable, size: int) -> Iterator[list]:
    if size < 1:
        raise ValueError("size must be >= 1")
    chunk = []
    for item in iterable:
        chunk.append(item)
        if len(chunk) == size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk
