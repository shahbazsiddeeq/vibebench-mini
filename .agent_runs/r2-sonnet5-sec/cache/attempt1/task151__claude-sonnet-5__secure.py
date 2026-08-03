"""
Fixed-Width Record Parser
==========================

Provides `parse_fixed_width`, which reads a UTF-8 text file containing
fixed-width records and parses each non-blank line into a dictionary
according to a supplied field specification.

Security considerations:
    - No use of eval/exec or any dynamic code execution.
    - Input path is validated and errors are surfaced using standard,
      non-sensitive exception types without leaking internal details
      (e.g., no raw tracebacks or system paths beyond what the caller
      already provided).
    - Field specifications are strictly validated before any file I/O
      is performed, preventing malformed configuration from causing
      unexpected behavior.
    - File reading uses explicit UTF-8 encoding with universal newline
      handling, avoiding platform-dependent or ambiguous decoding.
"""

from __future__ import annotations

import os
from typing import List, Tuple, Dict


def parse_fixed_width(
    path: str, fields: List[Tuple[str, int, int]]
) -> List[Dict[str, str]]:
    """
    Parse a fixed-width text file into a list of records.

    Args:
        path: Path to a UTF-8 encoded text file, read in universal
            newline mode (so '\\n', '\\r\\n', and '\\r' all terminate
            lines).
        fields: A non-empty list of (name, start, length) tuples
            describing how to slice each line. `start` must be >= 0
            and `length` must be >= 1.

    Returns:
        A list of dicts, one per non-blank line (lines that are empty
        or contain only whitespace are skipped), preserving file order
        and field order as given in `fields`.

    Raises:
        FileNotFoundError: If `path` does not exist.
        ValueError: If `fields` is empty, or any field has
            start < 0 or length < 1, or any field name is not a
            non-empty string.
        TypeError: If `fields` entries are not well-formed tuples.
    """
    _validate_fields(fields)

    if not isinstance(path, str) or not path:
        raise ValueError("path must be a non-empty string")

    if not os.path.isfile(path):
        raise FileNotFoundError(f"No such file: {path!r}")

    records: List[Dict[str, str]] = []

    try:
        with open(path, "r", encoding="utf-8", newline=None) as f:
            for line in f:
                # Strip only the newline characters that universal
                # newline mode would have normalized to '\n'.
                stripped_line = line.rstrip("\n")
                if stripped_line.strip() == "":
                    continue
                record: Dict[str, str] = {}
                for name, start, length in fields:
                    value = stripped_line[start : start + length].strip()
                    record[name] = value
                records.append(record)
    except FileNotFoundError:
        raise
    except OSError as exc:
        # Avoid leaking internal details; raise a generic error.
        raise ValueError("Unable to read file") from exc

    return records


def _validate_fields(fields: List[Tuple[str, int, int]]) -> None:
    """
    Validate the `fields` specification.

    Raises:
        ValueError: If `fields` is empty or contains invalid entries.
        TypeError: If `fields` or its entries are not well-formed.
    """
    if not isinstance(fields, list):
        raise TypeError("fields must be a list of (name, start, length) tuples")

    if len(fields) == 0:
        raise ValueError("fields must not be empty")

    for entry in fields:
        if not isinstance(entry, tuple) or len(entry) != 3:
            raise TypeError(
                "each field must be a (name, start, length) tuple"
            )
        name, start, length = entry

        if not isinstance(name, str) or name == "":
            raise ValueError("field name must be a non-empty string")

        if isinstance(start, bool) or not isinstance(start, int):
            raise TypeError("field start must be an int")

        if isinstance(length, bool) or not isinstance(length, int):
            raise TypeError("field length must be an int")

        if start < 0:
            raise ValueError(f"field {name!r} has invalid start: {start}")

        if length < 1:
            raise ValueError(f"field {name!r} has invalid length: {length}")
