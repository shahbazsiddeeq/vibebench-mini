"""
Duplicate File Finder
======================

Provides `find_duplicates(root)` which scans a directory tree and returns
a mapping of SHA-256 hex digest -> list of file paths sharing that content.

Security considerations:
- Input `root` is validated to be a string/path pointing to an existing
  directory before any filesystem operations occur.
- Symlinks are not followed to avoid infinite loops or escaping the
  intended directory tree.
- Files are read in fixed-size chunks to avoid loading arbitrarily large
  files fully into memory (mitigates resource-exhaustion issues).
- Filesystem errors (permission denied, broken symlinks, race conditions
  where a file disappears between listing and reading, etc.) are handled
  gracefully without leaking internal exception details or tracebacks to
  the caller; problematic files are simply skipped.
- No use of eval/exec or shell invocations; only the standard library
  `os` and `hashlib` modules are used.
"""

import hashlib
import os
from typing import Dict, List

_CHUNK_SIZE = 65536  # 64 KiB, reasonable balance of memory vs syscalls


def _hash_file(path: str) -> str:
    """
    Compute the SHA-256 hex digest of the file at `path`.

    Raises OSError (or subclasses) if the file cannot be read; callers
    are expected to handle/suppress such errors.
    """
    hasher = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(_CHUNK_SIZE)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()


def find_duplicates(root: str) -> Dict[str, List[str]]:
    """
    Scan the directory tree rooted at `root` and return a dict mapping
    SHA-256 hex digests to lists of file paths (only for digests shared
    by two or more files).

    Parameters
    ----------
    root : str
        Path to the directory to scan.

    Returns
    -------
    Dict[str, List[str]]
        Mapping of hex digest -> list of duplicate file paths. Empty
        dict if no duplicates are found or the directory is empty.

    Raises
    ------
    TypeError
        If `root` is not a string (or os.PathLike).
    ValueError
        If `root` does not exist or is not a directory.
    """
    if not isinstance(root, (str, os.PathLike)):
        raise TypeError("root must be a string or path-like object")

    root_str = os.fspath(root)

    if not os.path.exists(root_str):
        raise ValueError("root path does not exist")
    if not os.path.isdir(root_str):
        raise ValueError("root path is not a directory")

    hashes: Dict[str, List[str]] = {}

    # followlinks=False (default) avoids traversing symlinked directories,
    # which prevents infinite loops and unintended traversal outside root.
    for dirpath, dirnames, filenames in os.walk(root_str, followlinks=False):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)

            # Skip symlinked files to avoid hashing content outside the
            # intended tree or following malicious symlinks.
            try:
                if os.path.islink(file_path):
                    continue
                if not os.path.isfile(file_path):
                    continue
            except OSError:
                # Could not stat the path (e.g., permission denied);
                # skip it silently rather than exposing internal errors.
                continue

            try:
                digest = _hash_file(file_path)
            except (OSError, IOError):
                # File may have been deleted, permission denied, or is
                # otherwise unreadable; skip without raising.
                continue

            hashes.setdefault(digest, []).append(file_path)

    return {digest: paths for digest, paths in hashes.items() if len(paths) >= 2}
