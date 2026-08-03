"""Utilities for processing JSON Lines files."""

from __future__ import annotations

import json
import os
from typing import Union

PathType = Union[str, bytes, os.PathLike[str], os.PathLike[bytes]]


def _reject_non_finite(value: str) -> None:
    raise ValueError("non-finite JSON number")


def sum_jsonl(path: PathType, key: str) -> int | float:
    """Sum numeric values associated with *key* in a JSON Lines file.

    Missing keys, booleans, and non-numeric values are ignored. Blank lines are
    also ignored. A ValueError is raised if no matching numeric values exist.
    """
    if not isinstance(path, (str, bytes, os.PathLike)):
        raise TypeError("path must be a path-like value")
    if not isinstance(key, str):
        raise TypeError("key must be a string")

    total: int | float = 0
    found = False

    try:
        with open(path, "r", encoding="utf-8") as stream:
            for line in stream:
                if not line.strip():
                    continue

                try:
                    row = json.loads(line, parse_constant=_reject_non_finite)
                except (json.JSONDecodeError, ValueError) as exc:
                    raise ValueError("invalid JSON Lines data") from exc

                if not isinstance(row, dict):
                    continue

                value = row.get(key)
                if isinstance(value, bool) or not isinstance(value, (int, float)):
                    continue

                total += value
                found = True
    except (OSError, UnicodeError):
        raise

    if not found:
        raise ValueError(f"no numeric values found for key {key!r}")

    return total
