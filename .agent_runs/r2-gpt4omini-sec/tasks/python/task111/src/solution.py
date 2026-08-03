# src/solution.py

from typing import Iterable, List, Iterator

def chunked(iterable: Iterable, size: int) -> Iterator[List]:
    if not isinstance(size, int) or size < 1:
        raise ValueError("Size must be a positive integer greater than 0.")
    
    iterator = iter(iterable)
    while True:
        chunk = list()
        try:
            for _ in range(size):
                chunk.append(next(iterator))
        except StopIteration:
            if chunk:  # If there's any data in the chunk, yield it
                yield chunk
            break
        yield chunk
