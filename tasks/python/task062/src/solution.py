from __future__ import annotations

import hashlib
from collections import defaultdict
from pathlib import Path


def find_duplicates(root: str) -> dict[str, list[str]]:
    groups: dict[str, list[str]] = defaultdict(list)
    for f in Path(root).rglob("*"):
        if f.is_file():
            h = hashlib.sha256(f.read_bytes()).hexdigest()
            groups[h].append(str(f))
    return {h: sorted(paths) for h, paths in groups.items() if len(paths) >= 2}
