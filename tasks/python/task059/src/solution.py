from __future__ import annotations

from pathlib import Path


def tail(path: str, n: int) -> list[str]:
    if n < 0:
        raise ValueError("n must be non-negative")
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"No such file: {path}")
    lines = p.read_text(encoding="utf-8").splitlines()
    return lines[-n:] if n > 0 else []
