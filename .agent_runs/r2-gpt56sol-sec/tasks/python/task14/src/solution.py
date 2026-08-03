"""CSV deduplication utilities."""

from __future__ import annotations

import csv
import os
from typing import Optional


def dedupe_csv(
    in_path: str | os.PathLike[str],
    out_path: str | os.PathLike[str],
    key: str,
) -> int:
    """Keep the last CSV row for each distinct value in the named column.

    The output header matches the input header. Retained rows are ordered by
    the positions of their last occurrences in the input.

    Raises:
        KeyError: If *key* is not present in the header.
    """
    input_path = os.fspath(in_path)
    output_path = os.fspath(out_path)

    retained: dict[Optional[str], tuple[int, list[str]]] = {}

    with open(input_path, "r", encoding="utf-8-sig", newline="") as source:
        reader = csv.reader(source)

        try:
            header = next(reader)
        except StopIteration:
            raise KeyError(key) from None

        try:
            key_index = header.index(key)
        except ValueError:
            raise KeyError(key) from None

        for position, row in enumerate(reader):
            # Match csv.DictReader's treatment of physically blank lines.
            if not row:
                continue
            key_value: Optional[str] = (
                row[key_index] if key_index < len(row) else None
            )
            retained[key_value] = (position, row)

    ordered_rows = sorted(retained.values(), key=lambda item: item[0])

    with open(output_path, "w", encoding="utf-8", newline="") as destination:
        writer = csv.writer(destination)
        writer.writerow(header)
        writer.writerows(row for _, row in ordered_rows)

    return len(ordered_rows)
