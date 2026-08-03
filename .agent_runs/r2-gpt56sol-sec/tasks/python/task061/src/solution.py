"""Utilities for calculating directory sizes."""

from __future__ import annotations

import os
import stat
from typing import Union

PathType = Union[str, bytes, os.PathLike[str], os.PathLike[bytes]]


def dir_size(path: PathType) -> int:
    """Return the total byte size of regular files recursively under *path*.

    Symbolic links are neither followed nor counted.

    Raises:
        FileNotFoundError: If *path* does not exist.
        NotADirectoryError: If *path* is not a real directory.
    """
    root = os.fspath(path)
    root_stat = os.lstat(root)

    if not stat.S_ISDIR(root_stat.st_mode):
        raise NotADirectoryError(root)

    total = 0
    pending = [root]

    while pending:
        directory = pending.pop()

        with os.scandir(directory) as entries:
            for entry in entries:
                try:
                    entry_stat = entry.stat(follow_symlinks=False)
                except FileNotFoundError:
                    # The entry was removed concurrently.
                    continue

                mode = entry_stat.st_mode
                if stat.S_ISREG(mode):
                    total += entry_stat.st_size
                elif stat.S_ISDIR(mode):
                    pending.append(entry.path)

    return total
