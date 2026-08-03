"""
src/solution.py

Provides column_mean(path, col): compute the arithmetic mean of numeric
values found in a given CSV column, skipping rows where the value cannot
be parsed as a float.

Security considerations:
- No use of eval/exec.
- Only the standard library `csv` module is used for parsing, which
  handles quoting/escaping safely.
- File paths are validated to be strings; errors from the filesystem
  are caught and re-raised as generic ValueError to avoid leaking
  internal path/OS details.
- Column name is validated to be a non-empty string.
"""

import csv
from typing import Any


def column_mean(path: str, col: str) -> float:
    """
    Compute the arithmetic mean of numeric values in column `col` of the
    CSV file located at `path`.

    Rows whose value in `col` cannot be parsed as a float are skipped.

    Raises:
        ValueError: if inputs are invalid, the file cannot be read, the
            column is absent, or no numeric values are found.
    """
    if not isinstance(path, str) or not path.strip():
        raise ValueError("Invalid file path.")
    if not isinstance(col, str) or not col:
        raise ValueError("Invalid column name.")

    try:
        with open(path, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames is None or col not in reader.fieldnames:
                raise ValueError("Column not found in CSV header.")

            total = 0.0
            count = 0

            for row in reader:
                value: Any = row.get(col)
                if value is None:
                    continue
                value = value.strip()
                if not value:
                    continue
                try:
                    num = float(value)
                except (ValueError, TypeError):
                    continue
                total += num
                count += 1

    except ValueError:
        raise
    except OSError:
        raise ValueError("Unable to read the specified file.")
    except Exception:
        raise ValueError("Failed to process the CSV file.")

    if count == 0:
        raise ValueError("No numeric values found in the specified column.")

    return total / count
