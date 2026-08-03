"""
src/solution.py

Provides a secure, self-contained implementation of `sha256_file`, which
computes the SHA-256 hex digest of a file's contents.

Security considerations:
    - Input path is validated to be a non-empty string (or os.PathLike).
    - File is opened in binary mode and read in fixed-size chunks to
      avoid loading arbitrarily large files entirely into memory.
    - Errors are translated into standard, non-sensitive exceptions
      (FileNotFoundError, IsADirectoryError, TypeError, ValueError)
      without leaking internal details such as tracebacks or system paths
      beyond what the caller already provided.
    - No use of eval/exec, no shell invocation, no untrusted deserialization.
    - Only standard library modules are used (hashlib, os, pathlib).
"""

import hashlib
import os
from pathlib import Path

# Size of chunks read from the file at a time (64 KB).
_CHUNK_SIZE = 64 * 1024


def sha256_file(path) -> str:
    """
    Compute the SHA-256 hex digest of the contents of the file at `path`.

    Args:
        path: A string or os.PathLike object representing the file path.

    Returns:
        A 64-character lowercase hexadecimal string representing the
        SHA-256 digest of the file's contents.

    Raises:
        TypeError: If `path` is not a string or os.PathLike.
        ValueError: If `path` is empty.
        FileNotFoundError: If the file does not exist.
        IsADirectoryError: If `path` refers to a directory.
        PermissionError: If the file cannot be read due to permissions.
    """
    if not isinstance(path, (str, os.PathLike)):
        raise TypeError("path must be a string or os.PathLike object")

    # Normalize to a Path object for consistent handling.
    try:
        file_path = Path(path)
    except (TypeError, ValueError) as exc:
        raise ValueError("Invalid path provided") from exc

    if str(path).strip() == "":
        raise ValueError("path must not be empty")

    # Explicitly check existence to raise a clean FileNotFoundError,
    # rather than letting a lower-level OSError propagate with extra detail.
    if not file_path.exists():
        raise FileNotFoundError(f"No such file: {file_path}")

    if file_path.is_dir():
        raise IsADirectoryError(f"Path is a directory, not a file: {file_path}")

    hasher = hashlib.sha256()

    try:
        with open(file_path, "rb") as f:
            while True:
                chunk = f.read(_CHUNK_SIZE)
                if not chunk:
                    break
                hasher.update(chunk)
    except FileNotFoundError:
        # Race condition: file removed between exists() check and open().
        raise
    except IsADirectoryError:
        raise
    except PermissionError:
        raise
    except OSError as exc:
        # Catch-all for other OS-level errors without exposing internals.
        raise OSError("Unable to read file contents") from exc

    return hasher.hexdigest()
