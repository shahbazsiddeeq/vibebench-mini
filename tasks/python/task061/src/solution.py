from __future__ import annotations

from pathlib import Path


def dir_size(path: str) -> int:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"No such path: {path}")
    if not p.is_dir():
        raise NotADirectoryError(f"Not a directory: {path}")
    # Count only regular files. Symbolic links are neither followed nor counted.
    return sum(
        f.stat().st_size
        for f in p.rglob("*")
        if f.is_file() and not f.is_symlink()
    )
