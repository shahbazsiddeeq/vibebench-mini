import csv
from os import PathLike
from typing import Union

__all__ = ["csv_filter"]

Path = Union[str, PathLike[str]]


def csv_filter(in_path: Path, out_path: Path, column: str, value: str) -> int:
    """Write CSV rows whose specified column equals value and return their count."""
    with open(in_path, "r", newline="") as input_file:
        reader = csv.reader(input_file)

        try:
            header = next(reader)
        except StopIteration:
            raise KeyError(column) from None

        try:
            column_index = header.index(column)
        except ValueError:
            raise KeyError(column) from None

        count = 0
        with open(out_path, "w", newline="") as output_file:
            writer = csv.writer(output_file)
            writer.writerow(header)

            for row in reader:
                if column_index < len(row) and row[column_index] == value:
                    writer.writerow(row)
                    count += 1

    return count
