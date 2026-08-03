"""Deterministic SHA-256 hashing for directory trees."""

from __future__ import annotations

import hashlib
import os
import stat
from typing import Union

PathType = Union[str, os.PathLike[str]]


def dir_hash(path: PathType) -> str:
    """Return a deterministic SHA-256 digest for all regular files under path.

    Files are ordered by their relative POSIX paths. Symbolic links and other
    non-regular filesystem entries are ignored.

    Raises:
        ValueError: If path is invalid or is not an existing directory.
        OSError: If the directory or one of its files cannot be read.
    """
    try:
        root = os.fspath(path)
    except TypeError:
        raise ValueError("path must be a filesystem path") from None

    if not isinstance(root, str) or not root or "\x00" in root:
        raise ValueError("path must be a valid filesystem path")

    if not os.path.isdir(root):
        raise ValueError("path must be an existing directory")

    files: list[tuple[str, str]] = []

    def raise_walk_error(error: OSError) -> None:
        raise error

    for directory, _, names in os.walk(
        root, topdown=True, onerror=raise_walk_error, followlinks=False
    ):
        for name in names:
            full_path = os.path.join(directory, name)
            try:
                file_stat = os.stat(full_path, follow_symlinks=False)
            except FileNotFoundError:
                raise OSError("directory contents changed while hashing") from None

            if not stat.S_ISREG(file_stat.st_mode):
                continue

            relative = os.path.relpath(full_path, root)
            if os.sep != "/":
                relative = relative.replace(os.sep, "/")
            files.append((relative, full_path))

    files.sort(key=lambda item: item[0])

    digest = hashlib.sha256()
    for relative, full_path in files:
        try:
            path_bytes = relative.encode("utf-8")
        except UnicodeEncodeError:
            raise ValueError("a relative path is not valid UTF-8") from None

        with open(full_path, "rb") as file:
            content = file.read()

        digest.update(str(len(path_bytes)).encode("ascii"))
        digest.update(b":")
        digest.update(path_bytes)
        digest.update(str(len(content)).encode("ascii"))
        digest.update(b":")
        digest.update(content)

    return digest.hexdigest()
