import csv
from typing import Any, Dict


def dedupe_csv(in_path: str, out_path: str, key: str) -> int:
    with open(in_path, newline="", encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        if key not in rdr.fieldnames:
            raise KeyError(f"missing key column: {key}")
        last: Dict[str, Any] = {}
        order: Dict[str, int] = {}
        for idx, row in enumerate(rdr):
            k = row.get(key)
            last[k] = row
            order[k] = idx  # track index of last occurrence
    # write rows in ascending order of their last index (stable-ish, deterministic)
    items = sorted(last.items(), key=lambda kv: order[kv[0]])
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=rdr.fieldnames)  # type: ignore[attr-defined]
        w.writeheader()
        for _, row in items:
            w.writerow(row)
    return len(items)
