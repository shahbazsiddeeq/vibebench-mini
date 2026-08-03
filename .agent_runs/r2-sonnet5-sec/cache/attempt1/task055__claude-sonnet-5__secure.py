"""
src/solution.py

A small, secure utility for appending timestamped (or plain) lines to a
UTF-8 text log file, creating any missing parent directories as needed.
"""

from __future__ import annotations

import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Union


def append_log(path: Union[str, os.PathLike], message: str, timestamp: bool = True) -> None:
    """
    Append a single line to the UTF-8 text file at `path`.

    Args:
        path: Filesystem path (str or os.PathLike) of the log file to append to.
              Missing parent directories and the file itself are created.
        message: The text message to write. Must be a string.
        timestamp: If True (default), prefix the message with the current UTC
                   time formatted as ISO-8601 (seconds precision), followed by
                   a single space. If False, only the message is written.

    Returns:
        None

    Raises:
        TypeError: If `path` is not a str/os.PathLike or `message` is not a str,
                   or `timestamp` is not a bool.
        ValueError: If `path` is empty/blank or `message` contains embedded
                    newline characters.
        OSError: Propagated (re-raised) if the underlying filesystem operation
                 fails; no internal details beyond the standard OSError message
                 are exposed.
    """
    # --- Validate `path` ---
    if not isinstance(path, (str, os.PathLike)):
        raise TypeError("path must be a str or os.PathLike")

    path_str = os.fspath(path)
    if not isinstance(path_str, str) or not path_str.strip():
        raise ValueError("path must be a non-empty string")

    # --- Validate `message` ---
    if not isinstance(message, str):
        raise TypeError("message must be a string")

    if "\n" in message or "\r" in message:
        raise ValueError("message must not contain newline characters")

    # --- Validate `timestamp` ---
    if not isinstance(timestamp, bool):
        raise TypeError("timestamp must be a bool")

    # --- Build the line to append ---
    if timestamp:
        ts = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        line = f"{ts} {message}\n"
    else:
        line = f"{message}\n"

    # --- Resolve path and ensure parent directories exist ---
    target = Path(path_str)
    parent = target.parent
    try:
        if str(parent) not in ("", "."):
            parent.mkdir(parents=True, exist_ok=True)

        with open(target, mode="a", encoding="utf-8", newline="") as f:
            f.write(line)
    except OSError:
        # Re-raise without exposing internal details beyond the standard
        # OSError message (which itself is generally safe/informational).
        raise

    return None
