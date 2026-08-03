"""
src/solution.py

A small, security-conscious utility to compute the total size (in bytes)
of all regular files under a directory tree.

Design notes / security considerations:
- Input is validated before use (no blind trust of external path strings).
- Uses os.walk with followlinks=False so symlinked directories are not
  traversed (prevents symlink loops / escaping the intended tree).
- Symbolic links to files are explicitly skipped and never counted.
- Uses os.lstat (not os.stat) when inspecting entries to avoid following
  symlinks and to correctly detect them.
- No use of eval/exec, no shell invocation, no external randomness needed.
- Errors from the OS (permission issues, race conditions where a file
  disappears mid-walk) are handled gracefully rather than crashing with
  a raw traceback that could leak internal details.
"""

import os


def dir_size(path: str) -> int:
    """
    Compute the total size in bytes of all regular files under `path`,
    searched recursively.

    Args:
        path: Path to a directory.

    Returns:
        Total size in bytes of all regular files (symlinks excluded).

    Raises:
        FileNotFoundError: if `path` does not exist.
        NotADirectoryError: if `path` exists but is not a directory.
        TypeError: if `path` is not a string (or os.PathLike).
    """
    if not isinstance(path, (str, os.PathLike)):
        raise TypeError("path must be a string or os.PathLike object")

    # Normalize to string for consistent handling.
    path_str = os.fspath(path)

    # Validate existence and type up front. Use lstat so that a symlink
    # passed directly as `path` is reported based on its own type rather
    # than the target it points to (avoids surprising behavior).
    try:
        st = os.lstat(path_str)
    except FileNotFoundError:
        raise FileNotFoundError(f"path does not exist")
    except OSError:
        # Any other OS-level error accessing the path metadata.
        raise FileNotFoundError(f"path does not exist")

    if not os.path.isdir(path_str) or os.path.islink(path_str):
        raise NotADirectoryError(f"path is not a directory")

    total = 0

    # followlinks=False ensures symlinked directories are not descended into.
    for dirpath, dirnames, filenames in os.walk(path_str, followlinks=False):
        for name in filenames:
            full_path = os.path.join(dirpath, name)
            try:
                # Skip symbolic links entirely (files or dangling links).
                if os.path.islink(full_path):
                    continue
                entry_stat = os.lstat(full_path)
                # Only count regular files.
                if os.path.isfile(full_path) and not os.path.islink(full_path):
                    total += entry_stat.st_size
            except OSError:
                # File may have been removed/changed permissions mid-walk;
                # skip it rather than raising an internals-leaking error.
                continue

    return total
