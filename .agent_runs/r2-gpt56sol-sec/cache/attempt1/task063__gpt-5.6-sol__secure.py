"""Utilities for computing file hashes."""

from __future__ import annotations

import hashlib
import os
from typing import Union

PathLike = Union[str, bytes, os.PathLike[str], os.PathLike[bytes]]


def sha256_file(path: PathLike) -> str:
    """Return the lowercase hexadecimal SHA-256 digest of a file."""
    if not isinstance(path, (str, bytes, os.PathLike)):
        raise TypeError("path must be a string, bytes, or path-like object")

    digest = hashlib.sha256()
    with open(path, "rb") as file:
        for chunk in iter(lambda: file.read(128 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
