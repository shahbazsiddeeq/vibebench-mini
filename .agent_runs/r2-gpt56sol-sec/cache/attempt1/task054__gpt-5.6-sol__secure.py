"""Utilities for locating files by extension."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Union

PathInput = Union[str, os.PathLike[str]]


def find_by_ext(root: PathInput, ext: str) -> list[str]:
    """Return sorted, resolved paths of regular files matching an extension."""
    if not isinstance(ext, str):
        raise TypeError("ext must be a string")
    if not ext:
        raise ValueError("ext must not be empty")
    if "\x00" in ext:
        raise ValueError("ext contains an invalid character")

    try:
        root_value = os.fspath(root)
    except TypeError:
        raise TypeError("root must be a string or path-like object") from None

    if not isinstance(root_value, str):
        raise TypeError("root must resolve to a string path")
    if not root_value:
        raise ValueError("root must not be empty")
    if "\x00" in root_value:
        raise ValueError("root contains an invalid character")

    normalized_ext = ext if ext.startswith(".") else f".{ext}"

    try:
        root_path = Path(root_value).resolve()
        if not root_path.is_dir():
            return []
    except (OSError, RuntimeError):
        return []

    matches: list[str] = []

    for directory, _, filenames in os.walk(root_path, followlinks=False):
        for filename in filenames:
            if Path(filename).suffix != normalized_ext:
                continue

            candidate = Path(directory, filename)
            try:
                if candidate.is_file():
                    matches.append(str(candidate.resolve()))
            except (OSError, RuntimeError):
                continue

    matches.sort()
    return matches
