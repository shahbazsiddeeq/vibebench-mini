import os


def rotate_log(path: str, message: str, max_bytes: int, backup_count: int) -> None:
    """Append a log line to `path`, rotating by size like RotatingFileHandler."""
    if max_bytes < 1:
        raise ValueError("max_bytes must be >= 1")
    if backup_count < 0:
        raise ValueError("backup_count must be >= 0")

    line = message.encode("utf-8") + b"\n"
    line_size = len(line)

    current_size = os.path.getsize(path) if os.path.exists(path) else 0

    if current_size > 0 and current_size + line_size > max_bytes:
        _rotate(path, backup_count)

    with open(path, "ab") as f:
        f.write(line)


def _rotate(path: str, backup_count: int) -> None:
    if backup_count == 0:
        # No backups kept: discard the current file entirely.
        if os.path.exists(path):
            os.remove(path)
        return

    oldest = f"{path}.{backup_count}"
    if os.path.exists(oldest):
        os.remove(oldest)

    for i in range(backup_count - 1, 0, -1):
        src = f"{path}.{i}"
        if os.path.exists(src):
            os.replace(src, f"{path}.{i + 1}")

    os.replace(path, f"{path}.1")
