from os import PathLike
from typing import Union


def count_lines(path: Union[str, PathLike[str]]) -> int:
    """Return the number of lines in a UTF-8 encoded text file."""
    if not isinstance(path, (str, PathLike)):
        raise TypeError("path must be a string or path-like object")

    with open(path, mode="r", encoding="utf-8") as file:
        return sum(1 for _ in file)
