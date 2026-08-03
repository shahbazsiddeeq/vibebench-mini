"""
src/solution.py

Atomic file write utility.

Provides `atomic_write(path, content)` which writes `content` (a str, encoded
as UTF-8) to `path` atomically. The implementation:

  * Creates the parent directory tree if it does not already exist.
  * Writes the data to a temporary file created in the same directory as the
    destination (so the final `os.replace` is guaranteed to be an atomic
    rename on the same filesystem).
  * Flushes and fsyncs the temporary file's data before renaming it into
    place, and fsyncs the containing directory afterwards, so the write
    survives a crash.
  * Preserves the permission mode of an existing file at `path`; if no file
    exists yet, the new file gets the default mode (0o666 masked by the
    process umask).
  * Cleans up the temporary file on any error, leaving no artifacts behind.

Only the standard library is used.
"""

from __future__ import annotations

import os
import stat
import tempfile
from typing import Optional


def _fsync_dir(dir_path: str) -> None:
    """Fsync a directory so that renames/creates within it are durable."""
    dir_fd = os.open(dir_path, os.O_RDONLY)
    try:
        os.fsync(dir_fd)
    finally:
        os.close(dir_fd)


def atomic_write(path: str, content: str) -> None:
    """
    Atomically write `content` to `path`.

    Args:
        path: Destination file path.
        content: Text content to write (UTF-8 encoded).

    Raises:
        TypeError: If `path` is not a string or `content` is not a string.
        ValueError: If `path` is empty.
        OSError: Propagated from underlying filesystem operations on failure.
    """
    if not isinstance(path, str):
        raise TypeError("path must be a string")
    if not isinstance(content, str):
        raise TypeError("content must be a string")
    if path == "":
        raise ValueError("path must not be empty")

    # Resolve to an absolute-ish normalized form for directory operations,
    # but keep the original path for the final target name.
    abs_path = os.path.abspath(path)
    dir_name = os.path.dirname(abs_path)

    if dir_name and not os.path.isdir(dir_name):
        os.makedirs(dir_name, exist_ok=True)
    elif not dir_name:
        # No directory component resolved (shouldn't normally happen since
        # abspath always yields a directory), guard anyway.
        dir_name = "."

    # Determine existing file's mode, if any, so we can preserve it.
    existing_mode: Optional[int] = None
    try:
        st = os.stat(abs_path)
        existing_mode = stat.S_IMODE(st.st_mode)
    except FileNotFoundError:
        existing_mode = None
    except OSError:
        # Any other stat error: proceed as if file does not exist; the
        # subsequent replace will surface real problems.
        existing_mode = None

    tmp_fd = None
    tmp_path = None
    try:
        tmp_fd, tmp_path = tempfile.mkstemp(
            prefix=".atomic_write_",
            suffix=".tmp",
            dir=dir_name,
        )
        try:
            with os.fdopen(tmp_fd, "w", encoding="utf-8") as f:
                # fdopen takes ownership of tmp_fd; avoid double-close.
                tmp_fd = None
                f.write(content)
                f.flush()
                os.fsync(f.fileno())
        finally:
            # If fdopen succeeded, tmp_fd is None and the fd is already
            # closed by the context manager. If it failed before that,
            # tmp_fd might still be open and needs closing here.
            if tmp_fd is not None:
                os.close(tmp_fd)
                tmp_fd = None

        # Preserve permissions of an existing target file; otherwise leave
        # the temp file's default (umask-derived) mode as-is.
        if existing_mode is not None:
            os.chmod(tmp_path, existing_mode)

        os.replace(tmp_path, abs_path)
        tmp_path = None  # successfully moved; nothing left to clean up

        _fsync_dir(dir_name)
    except Exception:
        if tmp_path is not None and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except OSError:
                pass
        raise
