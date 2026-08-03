"""
src/solution.py

CSV Dedupe by Key (Keep Last).

Reads a CSV file with a header row and writes a new CSV file that
retains only the last occurrence of each distinct value found in a
specified key column. Order of output rows follows the position of
each key's *last* occurrence in the input file (ascending).

Security considerations:
    * Inputs are validated for type and basic sanity before use.
    * File I/O errors are caught and re-raised as generic, sanitized
      exceptions that do not leak internal paths or stack traces.
    * No use of eval/exec or other unsafe constructs.
    * Only the standard library is used.
"""

import csv
from typing import Any, Dict


def dedupe_csv(in_path: str, out_path: str, key: str) -> int:
    """
    Deduplicate rows of a CSV file by a key column, keeping the last
    occurrence of each distinct key value.

    Args:
        in_path: Path to the input CSV file (must have a header row).
        out_path: Path to write the deduplicated CSV output.
        key: Name of the column to deduplicate on.

    Returns:
        The number of data rows written to the output file.

    Raises:
        KeyError: If `key` is not present in the input CSV's header,
            including cases where the input file is empty or has no
            header row.
        TypeError: If arguments are not of the expected types.
        ValueError: If arguments are empty strings.
        RuntimeError: If reading or writing the CSV files fails due to
            an underlying I/O or CSV formatting error.
    """
    if not isinstance(in_path, str) or not isinstance(out_path, str) or not isinstance(key, str):
        raise TypeError("in_path, out_path, and key must be strings")

    if not in_path or not out_path or not key:
        raise ValueError("in_path, out_path, and key must be non-empty strings")

    fieldnames = None
    ordered: Dict[str, Dict[str, Any]] = {}

    try:
        with open(in_path, "r", encoding="utf-8", newline="") as infile:
            reader = csv.DictReader(infile)
            fieldnames = reader.fieldnames

            if not fieldnames or key not in fieldnames:
                raise KeyError(key)

            for row in reader:
                raw_value = row.get(key)
                value = raw_value if raw_value is not None else ""
                if value in ordered:
                    del ordered[value]
                ordered[value] = row
    except KeyError:
        raise
    except (OSError, csv.Error):
        raise RuntimeError("Failed to read input CSV file") from None

    try:
        with open(out_path, "w", encoding="utf-8", newline="") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in ordered.values():
                writer.writerow(row)
    except (OSError, csv.Error):
        raise RuntimeError("Failed to write output CSV file") from None

    return len(ordered)
