"""
src/solution.py

A small, secure, self-contained utility module implementing a lazy
chunked iterator.

Design notes (security-focused):
- No use of eval/exec or dynamic code execution.
- No external I/O, no network, no filesystem access.
- All inputs are validated defensively; invalid arguments raise clear,
  non-internal-detail-leaking exceptions.
- Uses only the Python standard library.
- Works lazily so it can safely operate on infinite/streaming iterables
  without excessive memory consumption.
"""

from typing import Any, Iterable, Iterator, List


def chunked(iterable: Iterable[Any], size: int) -> Iterator[List[Any]]:
    """
    Yield successive chunks (as lists) of up to `size` elements from
    `iterable`.

    Args:
        iterable: Any iterable (including infinite iterators) to be
            consumed lazily and split into chunks.
        size: Maximum number of elements per chunk. Must be an integer
            >= 1.

    Yields:
        Lists containing up to `size` consecutive elements from
        `iterable`. The final chunk may contain fewer than `size`
        elements if the iterable is exhausted.

    Raises:
        ValueError: If `size` is not an integer or is less than 1.
        TypeError: If `iterable` is not actually iterable.
    """
    # Validate `size` strictly: must be an int (bool is a subclass of
    # int, but using True/False as a chunk size is nonsensical and
    # potentially a caller error, so we reject non-int-like values but
    # still allow plain ints).
    if isinstance(size, bool) or not isinstance(size, int):
        raise ValueError("size must be an integer >= 1")
    if size < 1:
        raise ValueError("size must be >= 1")

    # Validate that `iterable` is actually iterable before proceeding.
    # This avoids leaking internal error details if a bad object is
    # passed and provides a clear, controlled error message instead.
    try:
        iterator = iter(iterable)
    except TypeError as exc:
        raise TypeError("iterable must be an iterable object") from exc

    def _generator() -> Iterator[List[Any]]:
        while True:
            chunk: List[Any] = []
            try:
                for _ in range(size):
                    chunk.append(next(iterator))
            except StopIteration:
                if chunk:
                    yield chunk
                return
            yield chunk

    return _generator()
