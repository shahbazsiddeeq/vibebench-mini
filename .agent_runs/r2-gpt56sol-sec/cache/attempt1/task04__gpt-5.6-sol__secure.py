"""Utilities for computing statistics from CSV files."""

from __future__ import annotations

import csv
import os
from typing import Union

PathLike = Union[str, bytes, os.PathLike[str], os.PathLike[bytes]]


def column_mean(path: PathLike, col: str) -> float:
    """Return the mean of values parseable as floats in a CSV column.

    The CSV file must contain a header row. Rows with missing or non-numeric
    values in the selected column are ignored. A ValueError is raised if the
    column is absent or contains no numeric values.
    """
    if not isinstance(path, (str, bytes, os.PathLike)):
        raise TypeError("path must be a path-like value")
    if not isinstance(col, str):
        raise TypeError("col must be a string")

    total = 0.0
    count = 0

    try:
        with open(path, "r", encoding="utf-8-sig", newline="") as csv_file:
            reader = csv.reader(csv_file)
            try:
                header = next(reader)
            except StopIteration:
                raise ValueError("CSV file has no header") from None

            try:
                column_index = header.index(col)
            except ValueError:
                raise ValueError("column not found") from None

            for row in reader:
                if column_index >= len(row):
                    continue
                try:
                    value = float(row[column_index])
                except (TypeError, ValueError, OverflowError):
                    continue

                total += value
                count += 1
    except csv.Error:
        raise ValueError("invalid CSV data") from None

    if count == 0:
        raise ValueError("column contains no numeric values")

    return total / count
