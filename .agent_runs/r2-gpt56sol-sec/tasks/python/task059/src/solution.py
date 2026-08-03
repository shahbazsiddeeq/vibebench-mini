"""Utilities for reading the end of text files."""

from collections import deque
from operator import index
from os import PathLike
from typing import Union


def tail(path: Union[str, bytes, PathLike], n: int) -> list[str]:
    """Return the last *n* lines from a UTF-8 text file without line endings.

    Raises:
        ValueError: If *n* is negative.
        TypeError: If *n* is not an integer or *path* is not path-like.
        FileNotFoundError: If *path* does not exist.
    """
    try:
        line_count = index(n)
    except TypeError:
        raise TypeError("n must be an integer") from None

    if line_count < 0:
        raise ValueError("n must be non-negative")

    if not isinstance(path, (str, bytes, PathLike)):
        raise TypeError("path must be a string, bytes, or path-like object")

    with open(path, "r", encoding="utf-8", newline=None) as file:
        if line_count == 0:
            return []

        lines = deque(file, maxlen=line_count)

    return [line[:-1] if line.endswith("\n") else line for line in lines]
