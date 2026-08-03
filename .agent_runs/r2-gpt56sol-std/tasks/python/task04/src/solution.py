import csv
import math
from os import PathLike
from typing import Union


def column_mean(path: Union[str, PathLike[str]], col: str) -> float:
    """Return the arithmetic mean of numeric values in a CSV column."""
    with open(path, "r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)

        if reader.fieldnames is None or col not in reader.fieldnames:
            raise ValueError(f"Column not found: {col}")

        total = 0.0
        count = 0

        for row in reader:
            try:
                value = float(row.get(col, ""))
            except (TypeError, ValueError):
                continue

            if not math.isfinite(value):
                continue

            total += value
            count += 1

    if count == 0:
        raise ValueError(f"No numeric values found in column: {col}")

    return total / count
