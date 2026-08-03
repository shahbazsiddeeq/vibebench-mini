"""
solution.py

Provides find_by_ext(root, ext): recursively find regular files under `root`
whose name ends with the given extension.
"""

import os
from pathlib import Path
from typing import List, Union


def find_by_ext(root: Union[str, os.PathLike], ext: str) -> List[str]:
    """
    Recursively find all regular files under `root` whose name ends with `ext`.

    Args:
        root: Directory to search (str or PathLike). May be relative or absolute.
        ext: File extension to match, with or without a leading dot (e.g. "py" or ".py").

    Returns:
        Sorted list of absolute, resolved file paths (as strings) that match.

    Raises:
        TypeError: if arguments are of the wrong type.
        ValueError: if root or ext is empty/invalid.
        NotADirectoryError: if root exists but is not a directory.
        FileNotFoundError: if root does not exist.
    """
    if not isinstance(root, (str, os.PathLike)):
        raise TypeError("root must be a string or os.PathLike")
    if not isinstance(ext, str):
        raise TypeError("ext must be a string")

    root_str = os.fspath(root)
    if not root_str or not root_str.strip():
        raise ValueError("root must be a non-empty path")

    ext = ext.strip()
    if not ext:
        raise ValueError("ext must be a non-empty string")

    # Normalize extension to always have a leading dot for matching.
    if not ext.startswith("."):
        ext = "." + ext

    # Basic sanity check: extension should not contain path separators.
    if os.sep in ext or (os.altsep and os.altsep in ext):
        raise ValueError("ext must not contain path separators")

    try:
        root_path = Path(root_str).resolve(strict=True)
    except FileNotFoundError:
        raise FileNotFoundError(f"root path does not exist")
    except OSError:
        raise ValueError("invalid root path")

    if not root_path.is_dir():
        raise NotADirectoryError("root must be a directory")

    matches: List[str] = []

    try:
        for dirpath, dirnames, filenames in os.walk(root_path, followlinks=False):
            for filename in filenames:
                if filename.endswith(ext):
                    full_path = Path(dirpath) / filename
                    # Ensure it's a regular file (not a broken symlink, device, etc.)
                    try:
                        if full_path.is_file():
                            matches.append(str(full_path.resolve()))
                    except OSError:
                        # Skip files we can't stat (permission issues, etc.)
                        continue
    except OSError:
        # Do not leak internal error details; return what we have or raise generic.
        raise RuntimeError("error while scanning directory")

    matches.sort()
    return matches
