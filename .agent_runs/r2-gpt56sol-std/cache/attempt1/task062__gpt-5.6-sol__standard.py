"""Utilities for finding files with identical content."""

from __future__ import annotations

import hashlib
import os
from collections import defaultdict
from typing import Dict, List, Union

PathLike = Union[str, os.PathLike[str]]


def _sha256_file(path: str, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as file:
        while chunk := file.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def find_duplicates(root: PathLike) -> Dict[str, List[str]]:
    """Return SHA-256 hashes mapped to paths for duplicate files under root."""
    root_path = os.fspath(root)
    files_by_hash: dict[str, list[str]] = defaultdict(list)

    for directory, subdirectories, filenames in os.walk(root_path):
        subdirectories.sort()
        filenames.sort()

        for filename in filenames:
            path = os.path.join(directory, filename)
            if os.path.isfile(path):
                files_by_hash[_sha256_file(path)].append(path)

    return {
        digest: paths
        for digest, paths in files_by_hash.items()
        if len(paths) >= 2
    }
