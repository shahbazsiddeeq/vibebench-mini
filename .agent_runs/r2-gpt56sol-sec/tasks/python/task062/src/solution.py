"""Utilities for locating files with identical content."""

from __future__ import annotations

import hashlib
import os
import stat
from collections import defaultdict
from typing import DefaultDict, Optional

__all__ = ["find_duplicates"]

_CHUNK_SIZE = 1024 * 1024


def _hash_regular_file(path: str) -> Optional[str]:
    """Return a stable SHA-256 digest for a regular file, or None on failure."""
    try:
        initial = os.lstat(path)
        if not stat.S_ISREG(initial.st_mode):
            return None

        flags = os.O_RDONLY
        flags |= getattr(os, "O_BINARY", 0)
        flags |= getattr(os, "O_CLOEXEC", 0)
        flags |= getattr(os, "O_NOFOLLOW", 0)

        descriptor = os.open(path, flags)
    except (OSError, ValueError):
        return None

    try:
        opened = os.fstat(descriptor)
        if not stat.S_ISREG(opened.st_mode):
            return None

        if (
            initial.st_dev != opened.st_dev
            or initial.st_ino != opened.st_ino
        ):
            return None

        digest = hashlib.sha256()
        while True:
            chunk = os.read(descriptor, _CHUNK_SIZE)
            if not chunk:
                break
            digest.update(chunk)

        final = os.fstat(descriptor)
        if (
            opened.st_dev != final.st_dev
            or opened.st_ino != final.st_ino
            or opened.st_size != final.st_size
            or opened.st_mtime_ns != final.st_mtime_ns
        ):
            return None

        return digest.hexdigest()
    except OSError:
        return None
    finally:
        try:
            os.close(descriptor)
        except OSError:
            pass


def find_duplicates(root: os.PathLike[str] | str) -> dict[str, list[str]]:
    """
    Find regular files beneath ``root`` that have identical content.

    The returned dictionary maps lowercase SHA-256 digests to sorted path
    lists. Only digests associated with at least two files are included.
    Symbolic links and files that cannot be read safely are ignored.
    """
    try:
        root_path = os.fspath(root)
    except TypeError:
        raise TypeError("root must be a string or path-like object") from None

    if not isinstance(root_path, str):
        raise TypeError("root must resolve to a string path")
    if not root_path or "\x00" in root_path:
        raise ValueError("root must be a non-empty valid path")

    grouped: DefaultDict[str, list[str]] = defaultdict(list)

    def ignore_walk_error(_: OSError) -> None:
        return None

    try:
        walker = os.walk(root_path, followlinks=False, onerror=ignore_walk_error)
        for directory, subdirectories, filenames in walker:
            subdirectories.sort()
            filenames.sort()

            for filename in filenames:
                path = os.path.join(directory, filename)
                digest = _hash_regular_file(path)
                if digest is not None:
                    grouped[digest].append(path)
    except (OSError, ValueError):
        return {}

    return {
        digest: sorted(paths)
        for digest, paths in grouped.items()
        if len(paths) >= 2
    }
