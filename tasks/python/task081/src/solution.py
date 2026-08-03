from __future__ import annotations


def diff_records(old: list[dict], new: list[dict], key: str) -> dict:
    for r in old + new:
        if key not in r:
            raise KeyError(f"key '{key}' missing from record: {r}")
    old_map = {r[key]: r for r in old}
    new_map = {r[key]: r for r in new}
    added = [r for k, r in new_map.items() if k not in old_map]
    removed = [r for k, r in old_map.items() if k not in new_map]
    changed = [r for k, r in new_map.items() if k in old_map and r != old_map[k]]
    return {"added": added, "removed": removed, "changed": changed}
