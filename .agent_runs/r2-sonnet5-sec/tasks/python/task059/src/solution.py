"""
File Tail (Last N Lines)

A secure implementation of a tail() function that returns the last N
lines of a file. Designed to avoid common pitfalls:
  - Validates all inputs (path type, n type/value).
  - Uses only standard library facilities.
  - Does not use eval/exec or any dynamic code execution.
  - Handles errors without leaking internal details (e.g., no raw
    tracebacks or system paths beyond what's necessary).
  - Reads the file safely with explicit encoding and error handling
    for malformed bytes.
"""

from collections import deque
from typing import List


def tail(path: str, n: int) -> List[str]:
    """
    Return the last `n` lines of the file at `path` as a list of strings
    (without trailing newlines). If `n` is greater than the number of
    lines in the file, all lines are returned.

    Args:
        path: Path to the file to read.
        n: Number of lines to return from the end of the file.

    Returns:
        A list of the last `n` lines (without newline characters).

    Raises:
        ValueError: If `n` is negative, or if `path`/`n` are of invalid types.
        FileNotFoundError: If the file at `path` does not exist.
        IsADirectoryError: If `path` refers to a directory rather than a file.
        PermissionError: If the file cannot be read due to permissions.
    """
    # --- Input validation -------------------------------------------------
    if not isinstance(path, str):
        raise ValueError("path must be a string")
    if not path.strip():
        raise ValueError("path must not be empty")

    if isinstance(n, bool) or not isinstance(n, int):
        # Explicitly reject bool (subclass of int) and non-int types.
        raise ValueError("n must be an integer")
    if n < 0:
        raise ValueError("n must be non-negative")

    if n == 0:
        # No need to touch the filesystem beyond confirming existence,
        # but to be consistent with error semantics (e.g., missing file
        # should still raise), we perform the existence check below.
        pass

    # --- Safe file access --------------------------------------------------
    try:
        with open(path, "r", encoding="utf-8", errors="replace", newline="") as f:
            if n == 0:
                # Still need to ensure the file is a valid, readable file.
                return []
            last_lines: deque = deque(maxlen=n)
            for raw_line in f:
                last_lines.append(raw_line)
    except FileNotFoundError:
        # Re-raise directly; message is generic enough not to leak internals.
        raise FileNotFoundError(f"No such file: {path!r}")
    except IsADirectoryError:
        raise IsADirectoryError(f"Expected a file, got a directory: {path!r}")
    except PermissionError:
        raise PermissionError(f"Permission denied: {path!r}")
    except OSError as exc:
        # Catch-all for other OS-level errors without exposing internal details.
        raise OSError("An error occurred while reading the file.") from None

    # Strip only the trailing newline characters (\n or \r\n), preserving
    # any other whitespace that might be meaningful content.
    result = [line.rstrip("\n").rstrip("\r") for line in last_lines]
    return result
