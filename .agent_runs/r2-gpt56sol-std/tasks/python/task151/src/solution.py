from typing import List, Tuple, Dict


def parse_fixed_width(
    path: str, fields: list[tuple[str, int, int]]
) -> list[dict[str, str]]:
    """Parse a UTF-8 text file containing fixed-width records."""
    if not fields:
        raise ValueError("fields must not be empty")

    for _, start, length in fields:
        if start < 0:
            raise ValueError("field start must be non-negative")
        if length < 1:
            raise ValueError("field length must be at least 1")

    records: list[dict[str, str]] = []

    with open(path, "r", encoding="utf-8", newline=None) as file:
        for line in file:
            if not line.strip():
                continue

            record = {
                name: line[start : start + length].strip()
                for name, start, length in fields
            }
            records.append(record)

    return records
