from collections import deque
from os import PathLike
from typing import Union


def tail(path: Union[str, PathLike[str]], n: int) -> list[str]:
    """Return the last *n* lines of a text file without trailing newlines."""
    if n < 0:
        raise ValueError("n must be non-negative")

    with open(path, "r") as file:
        if n == 0:
            return []

        lines = deque(maxlen=n)
        for line in file:
            lines.append(line[:-1] if line.endswith("\n") else line)

    return list(lines)
