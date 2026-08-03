import hashlib
import os
from pathlib import Path


def dir_hash(path: str) -> str:
    root = Path(path)
    if not root.is_dir():
        raise ValueError(f"{path} is not a directory")

    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        for name in filenames:
            full = Path(dirpath) / name
            if full.is_file():
                rel = full.relative_to(root).as_posix()
                files.append((rel, full))

    files.sort(key=lambda x: x[0])

    h = hashlib.sha256()
    for rel, full in files:
        rel_bytes = rel.encode("utf-8")
        content = full.read_bytes()
        h.update(f"{len(rel_bytes)}:".encode("utf-8"))
        h.update(rel_bytes)
        h.update(f"{len(content)}:".encode("utf-8"))
        h.update(content)

    return h.hexdigest()
