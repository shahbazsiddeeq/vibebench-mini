"""
src/solution.py

Provides csv_filter(in_path, out_path, column, value): filters rows of a CSV
file where the value in `column` equals `value`, writing matching rows
(including header) to `out_path`. Returns the count of matching data rows.

Security considerations:
- Only standard library modules are used.
- Input paths and parameters are validated for type correctness.
- No eval/exec or shell invocation is used.
- File operations use explicit encoding and newline handling to avoid
  platform-specific corruption or injection issues.
- Errors are raised with generic, non-sensitive messages to avoid leaking
  internal file system details.
"""

import csv
import os


def csv_filter(in_path: str, out_path: str, column: str, value: str) -> int:
    """
    Read CSV file at `in_path`, filter rows where `column` == `value`,
    and write matching rows (with header) to `out_path`.

    Args:
        in_path: Path to the input CSV file.
        out_path: Path to the output CSV file.
        column: Column name to filter on.
        value: Value to match against.

    Returns:
        Number of data rows written (excluding header).

    Raises:
        KeyError: If `column` is not present in the CSV header.
        TypeError: If arguments are not of expected types.
        ValueError: If paths are empty or invalid.
        FileNotFoundError: If the input file does not exist.
        IOError: For other I/O related failures (wrapped generically).
    """
    # --- Input validation ---
    if not isinstance(in_path, str) or not isinstance(out_path, str):
        raise TypeError("in_path and out_path must be strings")
    if not isinstance(column, str):
        raise TypeError("column must be a string")
    if value is not None and not isinstance(value, str):
        raise TypeError("value must be a string")

    if not in_path.strip():
        raise ValueError("in_path must not be empty")
    if not out_path.strip():
        raise ValueError("out_path must not be empty")

    # Normalize paths to avoid ambiguous relative path issues.
    in_path = os.fspath(in_path)
    out_path = os.fspath(out_path)

    if not os.path.isfile(in_path):
        raise FileNotFoundError("Input file not found")

    count = 0

    try:
        with open(in_path, "r", newline="", encoding="utf-8", errors="strict") as infile:
            reader = csv.DictReader(infile)
            fieldnames = reader.fieldnames

            if fieldnames is None:
                # Empty file: no header, no rows.
                fieldnames = []

            if column not in fieldnames:
                raise KeyError(column)

            with open(out_path, "w", newline="", encoding="utf-8") as outfile:
                writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                writer.writeheader()

                for row in reader:
                    # Defensive: ensure row is a dict with expected keys.
                    if row.get(column) == value:
                        writer.writerow(row)
                        count += 1
    except KeyError:
        raise
    except (OSError, csv.Error) as exc:
        # Avoid leaking internal details (paths, tracebacks) to caller.
        raise IOError("Failed to process CSV file") from exc

    return count
