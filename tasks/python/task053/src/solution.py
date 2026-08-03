from __future__ import annotations

from pathlib import Path


def count_lines(path: str) -> int:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"No such file: {path}")
    with p.open(encoding="utf-8") as f:
        return sum(1 for _ in f)
