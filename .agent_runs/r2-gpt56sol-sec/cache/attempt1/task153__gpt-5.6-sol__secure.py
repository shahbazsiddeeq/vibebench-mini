"""Generate SHA-256 checksum manifests for directory trees."""

from __future__ import annotations

import errno
import hashlib
import os
import stat
from typing import Optional


_CHUNK_SIZE = 1024 * 1024


def _hash_regular_file(path: str) -> Optional[str]:
    """Hash path if it is a non-symlink regular file."""
    initial = os.stat(path, follow_symlinks=False)
    if not stat.S_ISREG(initial.st_mode):
        return None

    flags = os.O_RDONLY
    flags |= getattr(os, "O_BINARY", 0)
    flags |= getattr(os, "O_CLOEXEC", 0)
    flags |= getattr(os, "O_NOFOLLOW", 0)
    flags |= getattr(os, "O_NONBLOCK", 0)

    fd = os.open(path, flags)
    try:
        opened = os.fstat(fd)
        current = os.stat(path, follow_symlinks=False)

        if not stat.S_ISREG(opened.st_mode) or not stat.S_ISREG(current.st_mode):
            return None

        if (
            opened.st_dev != current.st_dev
            or opened.st_ino != current.st_ino
        ):
            return None

        digest = hashlib.sha256()
        while True:
            chunk = os.read(fd, _CHUNK_SIZE)
            if not chunk:
                break
            digest.update(chunk)
        return digest.hexdigest()
    finally:
        os.close(fd)


def checksum_manifest(root: str) -> dict[str, str]:
    """Return a sorted mapping of relative file paths to SHA-256 digests."""
    root_path = os.fspath(root)
    if not isinstance(root_path, str):
        raise TypeError("root must be a string path")
    if not root_path:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), root_path)

    root_stat = os.stat(root_path, follow_symlinks=False)
    if not stat.S_ISDIR(root_stat.st_mode):
        raise NotADirectoryError(
            errno.ENOTDIR, os.strerror(errno.ENOTDIR), root_path
        )

    entries: list[tuple[str, str]] = []

    def raise_walk_error(error: OSError) -> None:
        raise error

    for directory, dirnames, filenames in os.walk(
        root_path, topdown=True, onerror=raise_walk_error, followlinks=False
    ):
        dirnames[:] = [
            name
            for name in dirnames
            if not os.path.islink(os.path.join(directory, name))
        ]

        for filename in filenames:
            full_path = os.path.join(directory, filename)
            digest = _hash_regular_file(full_path)
            if digest is None:
                continue

            relative_path = os.path.relpath(full_path, root_path)
            if os.sep != "/":
                relative_path = relative_path.replace(os.sep, "/")
            entries.append((relative_path, digest))

    entries.sort(key=lambda item: item[0])
    return dict(entries)
