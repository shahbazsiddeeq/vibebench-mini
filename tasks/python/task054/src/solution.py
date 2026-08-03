from __future__ import annotations

from pathlib import Path


def find_by_ext(root: str, ext: str) -> list[str]:
    if not ext.startswith("."):
        ext = "." + ext
    return sorted(str(p.resolve()) for p in Path(root).rglob(f"*{ext}") if p.is_file())
