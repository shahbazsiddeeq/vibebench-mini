from __future__ import annotations

import hashlib
from pathlib import Path


def sha256_file(path: str) -> str:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"No such file: {path}")
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()
