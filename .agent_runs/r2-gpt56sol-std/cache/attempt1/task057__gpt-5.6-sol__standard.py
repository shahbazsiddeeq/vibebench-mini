import json
from os import PathLike
from typing import Any, Iterable


def merge_json_files(
    paths: Iterable[str | PathLike[str]],
    output: str | PathLike[str],
) -> None:
    """Shallowly merge JSON objects from files and write the result as UTF-8 JSON."""
    merged: dict[str, Any] = {}

    for path in paths:
        with open(path, "r", encoding="utf-8") as source:
            data = json.load(source)

        if not isinstance(data, dict):
            raise ValueError(f"Top-level JSON value in {path!s} must be an object")

        merged.update(data)

    with open(output, "w", encoding="utf-8") as destination:
        json.dump(merged, destination, ensure_ascii=False)
