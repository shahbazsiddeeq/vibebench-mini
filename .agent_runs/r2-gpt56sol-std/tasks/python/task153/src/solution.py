"""Utilities for creating directory checksum manifests."""

from __future__ import annotations

import hashlib
import os
import stat


def checksum_manifest(root: str) -> dict[str, str]:
    """Return a sorted mapping of relative file paths to SHA-256 digests."""
    if not os.path.exists(root):
        raise FileNotFoundError(root)
    if not os.path.isdir(root):
        raise NotADirectoryError(root)

    entries: list[tuple[str, str]] = []

    for directory, _, filenames in os.walk(root, followlinks=False):
        for filename in filenames:
            path = os.path.join(directory, filename)

            try:
                mode = os.stat(path, follow_symlinks=False).st_mode
            except FileNotFoundError:
                raise

            if not stat.S_ISREG(mode):
                continue

            digest = hashlib.sha256()
            with open(path, "rb") as file:
                for chunk in iter(lambda: file.read(1024 * 1024), b""):
                    digest.update(chunk)

            relative_path = os.path.relpath(path, root).replace(os.sep, "/")
            entries.append((relative_path, digest.hexdigest()))

    return dict(sorted(entries))
