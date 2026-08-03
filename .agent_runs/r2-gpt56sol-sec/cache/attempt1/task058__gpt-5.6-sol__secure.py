"""Utilities for filtering CSV files."""

from __future__ import annotations

import csv
import os
import tempfile
from typing import Any


def csv_filter(
    in_path: str | os.PathLike[str],
    out_path: str | os.PathLike[str],
    column: str,
    value: Any,
) -> int:
    """Write rows whose selected column equals ``value`` and return their count.

    The output includes the original header. A ``KeyError`` is raised without
    modifying the output if ``column`` is absent from the header.
    """
    if not isinstance(column, str):
        raise TypeError("column must be a string")

    input_path = os.fspath(in_path)
    output_path = os.fspath(out_path)
    output_directory = os.path.dirname(os.path.abspath(output_path))

    temporary_path: str | bytes | None = None

    try:
        with open(input_path, "r", newline="", encoding="utf-8") as source:
            reader = csv.reader(source)
            header = next(reader, None)

            if header is None or column not in header:
                raise KeyError(column)

            column_index = header.index(column)
            descriptor, temporary_path = tempfile.mkstemp(
                prefix=".csv_filter_",
                dir=output_directory,
            )

            with os.fdopen(
                descriptor, "w", newline="", encoding="utf-8"
            ) as destination:
                writer = csv.writer(destination)
                writer.writerow(header)

                count = 0
                for row in reader:
                    if (
                        column_index < len(row)
                        and row[column_index] == value
                    ):
                        writer.writerow(row)
                        count += 1

        os.replace(temporary_path, output_path)
        temporary_path = None
        return count
    finally:
        if temporary_path is not None:
            try:
                os.unlink(temporary_path)
            except FileNotFoundError:
                pass
