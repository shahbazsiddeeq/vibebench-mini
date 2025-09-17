import csv
from statistics import mean


def column_mean(path: str, col: str) -> float:
    vals = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                vals.append(float(row[col]))
            except (KeyError, ValueError):
                continue
    if not vals:
        raise ValueError("no numeric values")
    return mean(vals)
