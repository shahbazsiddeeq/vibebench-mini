"""Secure path joining utilities."""

from __future__ import annotations

import os
from pathlib import Path, PureWindowsPath
from typing import Union

PathValue = Union[str, os.PathLike[str]]


def _coerce_path(value: PathValue, name: str) -> str:
    try:
        raw = os.fspath(value)
    except Exception:
        raise ValueError(f"{name} must be a valid path") from None

    if not isinstance(raw, str) or "\x00" in raw:
        raise ValueError(f"{name} must be a valid text path")
    if name == "base" and not raw:
        raise ValueError("base must not be empty")
    return raw


def safe_join(base: PathValue, user_path: PathValue) -> str:
    """Return a resolved path contained within *base*.

    Absolute user paths and paths that escape through parent components or
    symbolic links are rejected.
    """
    base_text = _coerce_path(base, "base")
    user_text = _coerce_path(user_path, "user_path")

    try:
        supplied = Path(user_text)

        # Also reject clearly absolute Windows paths when running on POSIX.
        if supplied.is_absolute() or PureWindowsPath(user_text).is_absolute():
            raise ValueError("absolute user paths are not allowed")

        resolved_base = Path(base_text).resolve(strict=False)
        resolved_target = (resolved_base / supplied).resolve(strict=False)

        try:
            resolved_target.relative_to(resolved_base)
        except ValueError:
            raise ValueError("path escapes the base directory") from None

        return str(resolved_target)
    except ValueError:
        raise
    except (OSError, RuntimeError):
        raise ValueError("unable to safely resolve path") from None
