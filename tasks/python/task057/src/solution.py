from __future__ import annotations

import json
from pathlib import Path


def merge_json_files(paths: list[str], output: str) -> None:
    merged: dict = {}
    for p in paths:
        data = json.loads(Path(p).read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError(f"{p} is not a JSON object")
        merged.update(data)
    Path(output).write_text(json.dumps(merged, indent=2), encoding="utf-8")
