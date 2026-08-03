import hashlib
from pathlib import Path


def dir_hash(path: str) -> str:
    root = Path(path)
    if not root.is_dir():
        raise ValueError(f"not a directory: {path}")
    h = hashlib.sha256()
    files = sorted(
        (p for p in root.rglob("*") if p.is_file()),
        key=lambda p: p.relative_to(root).as_posix(),
    )
    for p in files:
        rel = p.relative_to(root).as_posix().encode("utf-8")
        content = p.read_bytes()
        # Length-delimit each field so distinct trees cannot frame to the same
        # byte stream (e.g. a path/content boundary cannot be shifted).
        h.update(f"{len(rel)}:".encode("ascii"))
        h.update(rel)
        h.update(f"{len(content)}:".encode("ascii"))
        h.update(content)
    return h.hexdigest()
