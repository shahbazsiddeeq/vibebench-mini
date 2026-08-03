"""
JSONL Sum by Key

Provides `sum_jsonl(path, key)` which reads a JSON Lines file and sums the
numeric values found under `key` for each valid JSON object. Non-numeric or
missing values are ignored. If no numeric values are found, a ValueError
is raised.

The implementation is defensive:
 - Inputs are validated (types, non-empty strings).
 - File I/O errors are caught and re-raised as generic errors without
   leaking internal path/exception details.
 - JSON parsing errors on individual lines are skipped rather than
   crashing the whole operation.
 - Booleans are explicitly excluded from being treated as numeric,
   since `bool` is a subclass of `int` in Python but semantically not
   a number for this purpose.
 - `eval`/`exec` are never used; only `json.loads` is used for parsing.
"""

from __future__ import annotations

import json
import os
from numbers import Number
from typing import Union


def _is_numeric(value: object) -> bool:
    """Return True if value is a numeric type suitable for summation.

    Excludes booleans (which are technically ints in Python) and any
    non-Number types.
    """
    if isinstance(value, bool):
        return False
    return isinstance(value, Number)


def sum_jsonl(path: str, key: str) -> Union[int, float]:
    """Sum numeric values under `key` across all JSON objects in a JSONL file.

    Args:
        path: Path to a UTF-8 encoded JSON Lines file.
        key: The key whose numeric values should be summed.

    Returns:
        The sum of all numeric values found for `key`.

    Raises:
        ValueError: If inputs are invalid, the file cannot be read, or
            no numeric values are found for the given key.
    """
    if not isinstance(path, str) or not path.strip():
        raise ValueError("Invalid path provided.")
    if not isinstance(key, str) or not key:
        raise ValueError("Invalid key provided.")

    # Normalize path but do not expose internal filesystem details on error.
    safe_path = os.path.normpath(path)

    total: Union[int, float] = 0
    found_any = False

    try:
        with open(safe_path, "r", encoding="utf-8") as f:
            for line in f:
                stripped = line.strip()
                if not stripped:
                    continue
                try:
                    obj = json.loads(stripped)
                except (json.JSONDecodeError, ValueError):
                    # Skip malformed lines rather than failing entirely.
                    continue

                if not isinstance(obj, dict):
                    continue

                if key not in obj:
                    continue

                value = obj[key]
                if _is_numeric(value):
                    total += value
                    found_any = True
    except OSError:
        # Avoid leaking internal exception details (e.g., full paths, tracebacks).
        raise ValueError("Unable to read the specified file.")

    if not found_any:
        raise ValueError(f"No numeric values found for key '{key}'.")

    return total
