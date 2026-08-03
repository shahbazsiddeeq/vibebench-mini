"""Utilities for parsing fixed-width text records."""

from __future__ import annotations

from typing import Final

__all__: Final = ["parse_fixed_width"]


def parse_fixed_width(
    path: str,
    fields: list[tuple[str, int, int]],
) -> list[dict[str, str]]:
    """Parse non-blank fixed-width records from a UTF-8 text file."""
    if not isinstance(path, str):
        raise TypeError("path must be a string")
    if not isinstance(fields, list):
        raise TypeError("fields must be a list")

    field_specs = tuple(fields)
    if not field_specs:
        raise ValueError("fields must not be empty")

    validated: list[tuple[str, int, int]] = []
    for field in field_specs:
        if not isinstance(field, tuple) or len(field) != 3:
            raise TypeError("each field must be a (name, start, length) tuple")

        name, start, length = field

        if not isinstance(name, str):
            raise TypeError("field name must be a string")
        if isinstance(start, bool) or not isinstance(start, int):
            raise TypeError("field start must be an integer")
        if isinstance(length, bool) or not isinstance(length, int):
            raise TypeError("field length must be an integer")
        if start < 0:
            raise ValueError("field start must be non-negative")
        if length < 1:
            raise ValueError("field length must be at least 1")

        validated.append((name, start, length))

    records: list[dict[str, str]] = []

    with open(path, mode="r", encoding="utf-8", newline=None) as source:
        for line in source:
            if not line.strip():
                continue

            record: dict[str, str] = {}
            for name, start, length in validated:
                record[name] = line[start : start + length].strip()
            records.append(record)

    return records
