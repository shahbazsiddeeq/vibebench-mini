"""Size-based log rotation utilities."""

import os


def rotate_log(path: str, message: str, max_bytes: int, backup_count: int) -> None:
    """Append a UTF-8 log line, rotating the log first when required."""
    if not isinstance(path, str):
        raise TypeError("path must be a string")
    if not isinstance(message, str):
        raise TypeError("message must be a string")
    if not isinstance(max_bytes, int) or isinstance(max_bytes, bool):
        raise TypeError("max_bytes must be an integer")
    if not isinstance(backup_count, int) or isinstance(backup_count, bool):
        raise TypeError("backup_count must be an integer")
    if max_bytes < 1:
        raise ValueError("max_bytes must be at least 1")
    if backup_count < 0:
        raise ValueError("backup_count must be non-negative")

    line = message.encode("utf-8") + b"\n"
    truncate = False

    if os.path.exists(path):
        current_size = os.path.getsize(path)
        if current_size > 0 and current_size + len(line) > max_bytes:
            if backup_count == 0:
                truncate = True
            else:
                oldest_backup = f"{path}.{backup_count}"
                if os.path.lexists(oldest_backup):
                    os.remove(oldest_backup)

                for index in range(backup_count - 1, 0, -1):
                    source = f"{path}.{index}"
                    if os.path.lexists(source):
                        os.rename(source, f"{path}.{index + 1}")

                os.rename(path, f"{path}.1")

    mode = "wb" if truncate else "ab"
    with open(path, mode) as log_file:
        log_file.write(line)
