import json
from os import PathLike
from typing import Union


def sum_jsonl(path: Union[str, PathLike[str]], key: str) -> Union[int, float]:
    total: Union[int, float] = 0
    found = False

    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            if not line.strip():
                continue

            row = json.loads(line)
            if not isinstance(row, dict) or key not in row:
                continue

            value = row[key]
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                continue

            total += value
            found = True

    if not found:
        raise ValueError(f"no numeric values found for key {key!r}")

    return total
