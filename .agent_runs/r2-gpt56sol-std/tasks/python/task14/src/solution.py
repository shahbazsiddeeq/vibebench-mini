import csv
from os import PathLike
from typing import Union

Path = Union[str, PathLike[str]]


def dedupe_csv(in_path: Path, out_path: Path, key: str) -> int:
    """Keep only the last CSV row for each distinct value in ``key``."""
    with open(in_path, "r", encoding="utf-8", newline="") as source:
        reader = csv.reader(source)

        try:
            header = next(reader)
        except StopIteration:
            raise KeyError(key) from None

        if not header or key not in header:
            raise KeyError(key)

        key_index = header.index(key)
        last_rows: dict[object, tuple[int, list[str]]] = {}

        for position, row in enumerate(reader):
            key_value: object = row[key_index] if key_index < len(row) else None
            last_rows[key_value] = (position, row)

    ordered_rows = [
        row for _, row in sorted(last_rows.values(), key=lambda item: item[0])
    ]

    with open(out_path, "w", encoding="utf-8", newline="") as destination:
        writer = csv.writer(destination)
        writer.writerow(header)
        writer.writerows(ordered_rows)

    return len(ordered_rows)
