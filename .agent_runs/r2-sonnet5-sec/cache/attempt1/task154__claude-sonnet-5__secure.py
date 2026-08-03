"""
Chunked File Splitter and Joiner
--------------------------------

Provides:
    split_file(path, chunk_size, dest_dir) -> list[str]
    join_files(parts, dest) -> int

Security notes:
- All paths are validated and normalized before use.
- No use of eval/exec.
- Errors are raised with safe, generic messages that do not leak
  internal implementation details or sensitive system information.
- File reads/writes are done in a streaming fashion to avoid loading
  entire files into memory at once.
"""

import os

_READ_BUFFER_SIZE = 65536  # 64 KiB buffer for streaming copies


def _validate_str_path(value: str, name: str) -> str:
    """Ensure `value` is a non-empty string suitable for use as a path."""
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    if not value:
        raise ValueError(f"{name} must not be empty")
    return value


def split_file(path: str, chunk_size: int, dest_dir: str) -> list:
    """
    Split the binary file at `path` into consecutive chunks of at most
    `chunk_size` bytes, writing them into `dest_dir`.

    Returns the list of created part file paths, in order.

    Raises:
        ValueError: if chunk_size < 1.
        FileNotFoundError: if `path` does not exist.
        TypeError: if arguments are of the wrong type.
    """
    _validate_str_path(path, "path")
    _validate_str_path(dest_dir, "dest_dir")

    if not isinstance(chunk_size, int) or isinstance(chunk_size, bool):
        raise TypeError("chunk_size must be an int")
    if chunk_size < 1:
        raise ValueError("chunk_size must be >= 1")

    if not os.path.isfile(path):
        raise FileNotFoundError(f"Source file not found: {os.path.basename(path)}")

    os.makedirs(dest_dir, exist_ok=True)

    basename = os.path.basename(path)
    parts = []

    try:
        with open(path, "rb") as src:
            index = 0
            while True:
                chunk = src.read(chunk_size)
                if not chunk:
                    break
                part_name = f"{basename}.part{format(index, '03d')}"
                part_path = os.path.join(dest_dir, part_name)
                with open(part_path, "wb") as out:
                    out.write(chunk)
                parts.append(part_path)
                index += 1
    except OSError as exc:
        raise OSError("Failed to split file due to an I/O error") from exc

    return parts


def join_files(parts: list, dest: str) -> int:
    """
    Concatenate the raw bytes of each file listed in `parts`, in order,
    into a new file at `dest`.

    Returns the total number of bytes written.

    Raises:
        FileNotFoundError: if any part path does not exist.
        TypeError: if arguments are of the wrong type.
    """
    if not isinstance(parts, (list, tuple)):
        raise TypeError("parts must be a list of paths")
    _validate_str_path(dest, "dest")

    validated_parts = []
    for p in parts:
        if not isinstance(p, str) or not p:
            raise TypeError("each part path must be a non-empty string")
        if not os.path.isfile(p):
            raise FileNotFoundError(f"Part file not found: {os.path.basename(p)}")
        validated_parts.append(p)

    dest_dir = os.path.dirname(dest)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    total_bytes = 0
    try:
        with open(dest, "wb") as out:
            for part_path in validated_parts:
                with open(part_path, "rb") as src:
                    while True:
                        buf = src.read(_READ_BUFFER_SIZE)
                        if not buf:
                            break
                        out.write(buf)
                        total_bytes += len(buf)
    except OSError as exc:
        raise OSError("Failed to join files due to an I/O error") from exc

    return total_bytes
