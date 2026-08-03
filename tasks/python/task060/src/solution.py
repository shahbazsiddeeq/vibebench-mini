from __future__ import annotations

import os
import stat
import tempfile
from pathlib import Path


def atomic_write(path: str, content: str) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)

    # Determine the permission mode for the final file. If it already exists,
    # preserve its mode; otherwise use the process default (0666 & ~umask).
    try:
        target_mode = stat.S_IMODE(os.stat(path).st_mode)
    except FileNotFoundError:
        umask = os.umask(0)
        os.umask(umask)
        target_mode = 0o666 & ~umask

    fd, tmp = tempfile.mkstemp(dir=p.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(content)
            f.flush()
            os.fsync(f.fileno())
        os.chmod(tmp, target_mode)
        os.replace(tmp, path)
    except Exception:
        os.unlink(tmp)
        raise

    # Ensure the rename itself is durable by fsyncing the parent directory.
    dir_fd = os.open(str(p.parent), os.O_RDONLY)
    try:
        os.fsync(dir_fd)
    finally:
        os.close(dir_fd)
