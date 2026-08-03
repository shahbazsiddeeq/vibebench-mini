"""
Directory Checksum Manifest

Provides `checksum_manifest(root: str) -> dict[str, str]` which walks a
directory tree and returns a manifest mapping relative file paths (using
POSIX '/' separators) to the lowercase hex SHA-256 digest of each file's
contents. Symbolic links are not followed. The returned dict is ordered
by key ascending.
"""

from __future__ import annotations

import hashlib
import os

_CHUNK_SIZE = 65536  # 64 KiB


def _hash_file(path: str) -> str:
    """Compute the lowercase hex SHA-256 digest of a file's contents.

    Streams the file in fixed-size chunks so large files do not need to
    fit entirely in memory. Errors are not swallowed silently but are
    re-raised without leaking internal details beyond the OS-provided
    exception (e.g. permission errors, missing file due to race conditions).
    """
    hasher = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            chunk = fh.read(_CHUNK_SIZE)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()


def checksum_manifest(root: str) -> dict[str, str]:
    """Walk the directory tree rooted at `root` and build a checksum manifest.

    Parameters
    ----------
    root : str
        Path to the directory to scan.

    Returns
    -------
    dict[str, str]
        Mapping of relative file path (POSIX separators) -> lowercase hex
        SHA-256 digest, sorted ascending by key.

    Raises
    ------
    FileNotFoundError
        If `root` does not exist.
    NotADirectoryError
        If `root` exists but is not a directory.
    """
    if not isinstance(root, str):
        raise TypeError("root must be a string")

    # Validate root existence/type up front, without following symlinks
    # for the root itself in a way that would misreport type; standard
    # os.path checks are sufficient here.
    if not os.path.exists(root):
        raise FileNotFoundError(f"root path does not exist: {root!r}")
    if not os.path.isdir(root):
        raise NotADirectoryError(f"root path is not a directory: {root!r}")

    manifest: dict[str, str] = {}

    # followlinks=False (the default) ensures symlinked directories are
    # not traversed. os.walk also reports symlinked files in `filenames`
    # but we explicitly skip anything that is a symlink to avoid
    # following them for hashing purposes.
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        # Ensure symlinked directories are not descended into even if
        # some platform/version quirk includes them; filter defensively.
        dirnames[:] = [
            d for d in dirnames
            if not os.path.islink(os.path.join(dirpath, d))
        ]

        for filename in filenames:
            full_path = os.path.join(dirpath, filename)

            # Skip symbolic links (including symlinked files) entirely.
            if os.path.islink(full_path):
                continue

            # Only process regular files.
            if not os.path.isfile(full_path):
                continue

            rel_path = os.path.relpath(full_path, root)
            rel_key = rel_path.replace(os.sep, "/")

            digest = _hash_file(full_path)
            manifest[rel_key] = digest

    return dict(sorted(manifest.items(), key=lambda item: item[0]))
