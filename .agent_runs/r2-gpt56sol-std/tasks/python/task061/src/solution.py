"""Utilities for calculating directory sizes."""

import os
import stat
from typing import Union

PathType = Union[str, bytes, os.PathLike]


def dir_size(path: PathType) -> int:
    """Return the total size of regular files recursively contained in *path*.

    Symbolic links are ignored and never followed.
    """
    root = os.fspath(path)
    root_stat = os.stat(root, follow_symlinks=False)

    if not stat.S_ISDIR(root_stat.st_mode):
        raise NotADirectoryError(root)

    total = 0
    pending = [root]

    while pending:
        directory = pending.pop()
        with os.scandir(directory) as entries:
            for entry in entries:
                entry_stat = entry.stat(follow_symlinks=False)

                if stat.S_ISREG(entry_stat.st_mode):
                    total += entry_stat.st_size
                elif stat.S_ISDIR(entry_stat.st_mode):
                    pending.append(entry.path)

    return total
