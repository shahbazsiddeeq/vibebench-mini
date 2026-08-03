"""
src/solution.py

Provides a secure `safe_join` function that joins a base directory with a
user-supplied relative path, ensuring the resulting path cannot escape the
base directory via path traversal (`..`), symlinks, absolute paths, or
other tricks.

Only the standard library is used.
"""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import List


__all__ = ["safe_join"]


def _split_parts(user_path: str) -> List[str]:
    """
    Split a user-supplied path into its components, normalizing both
    forward and backward slashes as separators. Empty and '.' components
    are dropped (they are harmless no-ops).
    """
    # Treat both '/' and '\' as separators regardless of platform, since a
    # malicious input could use either to attempt traversal.
    raw_parts = re.split(r"[\\/]+", user_path)
    return [p for p in raw_parts if p not in ("", ".")]


def _is_within(path: Path, base: Path) -> bool:
    """
    Return True if `path` is equal to `base` or is a descendant of `base`.
    Both paths are expected to be absolute and already resolved.
    """
    try:
        path.relative_to(base)
        return True
    except ValueError:
        return False


def safe_join(base: str, user_path: str) -> str:
    """
    Safely join `base` and `user_path`, returning a string path that is
    guaranteed to reside within `base`.

    Raises:
        ValueError: if inputs are invalid, the resulting path would escape
            `base` (via `..`, an absolute path, or a symlink), or `base`
            does not exist / cannot be resolved.
    """
    # --- Basic type validation -------------------------------------------------
    if not isinstance(base, str) or not isinstance(user_path, str):
        raise ValueError("Invalid path arguments.")

    # --- Reject dangerous / malformed input -------------------------------------
    if "\x00" in base or "\x00" in user_path:
        raise ValueError("Null bytes are not allowed in paths.")

    if os.path.isabs(user_path):
        raise ValueError("Absolute paths are not allowed.")

    # Reject Windows-style drive specifiers (e.g. "C:\\...") even on POSIX,
    # since they could be misinterpreted downstream.
    if re.match(r"^[A-Za-z]:", user_path):
        raise ValueError("Drive-letter paths are not allowed.")

    # --- Resolve the base directory ---------------------------------------------
    try:
        base_real = Path(base).resolve(strict=True)
    except (OSError, RuntimeError):
        raise ValueError("Invalid base directory.")

    if not base_real.is_dir():
        raise ValueError("Base path is not a directory.")

    # --- Walk the path components, checking for symlink escapes as we go -------
    parts = _split_parts(user_path)

    candidate = base_real
    for part in parts:
        if part == "..":
            # Moving up is allowed as long as the final result stays within
            # base_real; we still update candidate so later segments are
            # resolved relative to the correct (possibly higher) directory.
            candidate = candidate.parent
            continue

        # Reject any other suspicious components defensively.
        if part in ("", "."):
            continue

        candidate = candidate / part

        try:
            if candidate.is_symlink():
                target = candidate.resolve(strict=False)
                if not _is_within(target, base_real):
                    raise ValueError("Path traversal via symlink detected.")
                candidate = target
        except OSError:
            # If we cannot introspect the symlink safely, fail closed.
            raise ValueError("Unable to validate path component.")

    # --- Final resolution and containment check ---------------------------------
    try:
        if candidate.exists():
            final = candidate.resolve(strict=True)
        else:
            # For non-existent paths, resolve only the existing parents.
            final = candidate.resolve(strict=False)
    except OSError:
        raise ValueError("Unable to resolve final path.")

    if not _is_within(final, base_real):
        raise ValueError("Resulting path escapes the base directory.")

    return str(final)
