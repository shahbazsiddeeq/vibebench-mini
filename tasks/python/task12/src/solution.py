import hashlib
from pathlib import Path


def dir_hash(path: str) -> str:
    root = Path(path)
    h = hashlib.sha256()
    for p in sorted([p for p in root.rglob("*") if p.is_file()]):
        rel = p.relative_to(root).as_posix()
        h.update(rel.encode("utf-8"))
        h.update(b"\n")
        h.update(p.read_bytes())
        h.update(b"\n")
    return h.hexdigest()
