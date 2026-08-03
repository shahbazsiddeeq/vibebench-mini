"""
Safe path joining utility.

Provides safe_join(base, user_path) which joins a base directory with a
user-supplied path fragment and guarantees that the resulting path stays
within the base directory. This protects against classic path traversal
attacks (e.g. "../../etc/passwd") as well as symlink-based escapes, since
the final path is fully resolved (symlinks followed) before the containment
check is performed.

Only the Python standard library is used.
"""

from __future__ import annotations

import os
from pathlib import Path


def safe_join(base: str, user_path: str) -> str:
    """Safely join `user_path` onto `base`, returning a resolved path.

    Raises:
        ValueError: if the resulting path would escape `base`, whether via
            "../" traversal, an absolute path override, or a symlink that
            points outside of `base`.
    """
    if user_path is None:
        raise ValueError("user_path must not be None")

    base_path = Path(base).resolve()

    # Reject absolute user-supplied paths outright: joining an absolute
    # path with Path(base) would otherwise discard the base entirely.
    user_path_obj = Path(user_path)
    if user_path_obj.is_absolute() or (os.name == "nt" and user_path_obj.drive):
        raise ValueError("Absolute paths are not allowed")

    candidate = base_path / user_path_obj

    # Resolve fully (this follows symlinks and normalizes '..' segments).
    # strict=False allows the target to not yet exist.
    resolved = candidate.resolve(strict=False)

    try:
        resolved.relative_to(base_path)
    except ValueError:
        raise ValueError(
            f"Path traversal attempt detected: '{user_path}' escapes base '{base}'"
        )

    return str(resolved)
