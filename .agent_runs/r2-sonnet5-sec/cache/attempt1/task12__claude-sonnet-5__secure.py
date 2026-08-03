"""
Deterministic directory hashing utility.

This module provides `dir_hash(path)`, which computes a stable SHA-256
digest over the contents of a directory tree. The implementation is
careful to:

  * Validate all inputs (path must exist and be a directory).
  * Avoid any use of eval/exec or shell invocation.
  * Sort files deterministically by their relative POSIX path so the
    result does not depend on filesystem iteration order.
  * Use length-prefixed framing for both path and content to prevent
    ambiguity/collision from boundary-shifting attacks.
  * Avoid leaking internal exception details; only well-defined
    exceptions (ValueError) are raised to callers.
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path, PurePosixPath
from typing import List


def _collect_files(root: Path) -> List[Path]:
    """Recursively collect all regular files under root.

    Symlinks are not followed to avoid escaping the intended tree or
    infinite loops; only regular files are included.
    """
    files: List[Path] = []
    try:
        for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
            # Keep dirnames traversal deterministic-ish; sorting here is
            # not strictly required for correctness since we sort the
            # final file list, but it avoids relying on OS ordering.
            dirnames.sort()
            for name in filenames:
                full_path = Path(dirpath) / name
                # Only include regular files (skip symlinks, sockets, etc.)
                if full_path.is_symlink():
                    continue
                if full_path.is_file():
                    files.append(full_path)
    except OSError as exc:
        # Do not leak internal filesystem error details; surface a
        # generic, safe error instead.
        raise ValueError("Unable to read directory contents") from exc

    return files


def dir_hash(path: str) -> str:
    """Compute a deterministic SHA-256 hex digest of a directory tree.

    The hash is computed over all regular files found recursively under
    `path`, sorted by their relative POSIX path. For each file, the
    following bytes are fed into a single SHA-256 hash, in order:

        len(utf8(relative_path)) as ascii decimal digits, then b":"
        utf8(relative_path) bytes
        len(content) as ascii decimal digits, then b":"
        content bytes

    Raises:
        ValueError: if `path` does not exist or is not a directory.
    """
    if not isinstance(path, str):
        raise ValueError("path must be a string")

    try:
        root = Path(path)
    except (TypeError, ValueError) as exc:
        raise ValueError("Invalid path") from exc

    try:
        if not root.is_dir():
            raise ValueError("path is not a directory")
    except OSError as exc:
        raise ValueError("Unable to access path") from exc

    try:
        resolved_root = root.resolve(strict=True)
    except OSError as exc:
        raise ValueError("Unable to resolve path") from exc

    files = _collect_files(resolved_root)

    # Build (relative_posix_path, absolute_path) pairs.
    entries = []
    for f in files:
        try:
            rel = f.relative_to(resolved_root)
        except ValueError:
            # Should not happen since files come from walking resolved_root,
            # but guard defensively.
            continue
        rel_posix = PurePosixPath(*rel.parts).as_posix()
        entries.append((rel_posix, f))

    # Sort deterministically by relative POSIX path.
    entries.sort(key=lambda item: item[0])

    hasher = hashlib.sha256()

    for rel_posix, full_path in entries:
        rel_bytes = rel_posix.encode("utf-8")
        try:
            content = full_path.read_bytes()
        except OSError as exc:
            raise ValueError("Unable to read file contents") from exc

        hasher.update(str(len(rel_bytes)).encode("ascii"))
        hasher.update(b":")
        hasher.update(rel_bytes)
        hasher.update(str(len(content)).encode("ascii"))
        hasher.update(b":")
        hasher.update(content)

    return hasher.hexdigest()
