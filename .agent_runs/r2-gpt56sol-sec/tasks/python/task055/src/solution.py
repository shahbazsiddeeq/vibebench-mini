from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Union

PathLike = Union[str, os.PathLike[str]]


def append_log(path: PathLike, message: str, timestamp: bool = True) -> None:
    """Append one UTF-8 encoded, newline-terminated log entry to *path*."""
    if not isinstance(message, str):
        raise TypeError("message must be a string")
    if "\n" in message or "\r" in message:
        raise ValueError("message must not contain newline characters")
    if not isinstance(timestamp, bool):
        raise TypeError("timestamp must be a boolean")

    try:
        file_path = os.fspath(path)
    except TypeError:
        raise TypeError("path must be a string or path-like object") from None

    if not isinstance(file_path, str):
        raise TypeError("path must resolve to a string")
    if not file_path or "\x00" in file_path:
        raise ValueError("path must be a non-empty valid path")

    parent = os.path.dirname(os.path.abspath(file_path))
    os.makedirs(parent, exist_ok=True)

    if timestamp:
        current_time = datetime.now(timezone.utc).isoformat(timespec="seconds")
        line = f"{current_time} {message}\n"
    else:
        line = f"{message}\n"

    with open(file_path, mode="a", encoding="utf-8", newline="") as log_file:
        log_file.write(line)
