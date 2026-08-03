"""
Size-Based Log Rotator

Provides rotate_log(path, message, max_bytes, backup_count) which appends a
line to a log file, rotating existing backups when the new line would push
the file past max_bytes.
"""

import os


def _validate_inputs(path: str, message: str, max_bytes: int, backup_count: int) -> None:
    if not isinstance(path, str) or not path:
        raise ValueError("path must be a non-empty string")
    if not isinstance(message, str):
        raise ValueError("message must be a string")
    if isinstance(max_bytes, bool) or not isinstance(max_bytes, int):
        raise ValueError("max_bytes must be an integer")
    if isinstance(backup_count, bool) or not isinstance(backup_count, int):
        raise ValueError("backup_count must be an integer")
    if max_bytes < 1:
        raise ValueError("max_bytes must be >= 1")
    if backup_count < 0:
        raise ValueError("backup_count must be >= 0")


def _safe_getsize(path: str) -> int:
    try:
        return os.path.getsize(path)
    except OSError:
        return 0


def _rotate(path: str, backup_count: int) -> None:
    if backup_count == 0:
        try:
            with open(path, "wb"):
                pass
        except OSError as exc:
            raise RuntimeError("Failed to truncate log file") from exc
        return

    # Remove the oldest backup if present.
    oldest = f"{path}.{backup_count}"
    if os.path.exists(oldest):
        try:
            os.remove(oldest)
        except OSError as exc:
            raise RuntimeError("Failed to remove old backup file") from exc

    # Shift existing backups up by one.
    for i in range(backup_count - 1, 0, -1):
        src = f"{path}.{i}"
        dst = f"{path}.{i + 1}"
        if os.path.exists(src):
            try:
                os.rename(src, dst)
            except OSError as exc:
                raise RuntimeError("Failed to rotate backup file") from exc

    # Move current file to .1
    try:
        os.rename(path, f"{path}.1")
    except OSError as exc:
        raise RuntimeError("Failed to rotate current log file") from exc


def rotate_log(path: str, message: str, max_bytes: int, backup_count: int) -> None:
    """
    Append one log line to `path`, rotating first if needed.

    Raises:
        ValueError: if inputs are invalid.
    """
    _validate_inputs(path, message, max_bytes, backup_count)

    line = message.encode("utf-8") + b"\n"
    line_size = len(line)

    try:
        exists = os.path.exists(path)
        current_size = _safe_getsize(path) if exists else 0

        if exists and current_size > 0 and (current_size + line_size) > max_bytes:
            _rotate(path, backup_count)

        with open(path, "ab") as f:
            f.write(line)
    except (OSError, RuntimeError) as exc:
        raise RuntimeError("Failed to rotate/write log file") from exc
