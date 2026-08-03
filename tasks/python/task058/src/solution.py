from __future__ import annotations

import csv


def csv_filter(in_path: str, out_path: str, column: str, value: str) -> int:
    with open(in_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None or column not in reader.fieldnames:
            raise KeyError(f"column '{column}' not in header")
        rows = [row for row in reader if row[column] == value]
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)
