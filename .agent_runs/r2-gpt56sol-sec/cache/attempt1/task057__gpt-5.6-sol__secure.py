"""Utilities for merging JSON files."""

from __future__ import annotations

import json
import os
from collections.abc import Iterable
from typing import Any


def merge_json_files(
    paths: Iterable[str | os.PathLike[str]],
    output: str | os.PathLike[str],
) -> None:
    """Shallowly merge JSON objects from files and write the result.

    Files are processed in order, with later top-level keys replacing earlier
    ones. Each input file must contain a JSON object.
    """
    if isinstance(paths, (str, bytes, os.PathLike)) or not isinstance(paths, Iterable):
        raise TypeError("paths must be an iterable of file paths")

    try:
        output_path = os.fspath(output)
    except TypeError as exc:
        raise TypeError("output must be a valid file path") from exc

    if not isinstance(output_path, (str, bytes)):
        raise TypeError("output must be a valid file path")

    merged: dict[str, Any] = {}

    for path in paths:
        try:
            input_path = os.fspath(path)
        except TypeError as exc:
            raise TypeError("each input path must be a valid file path") from exc

        if not isinstance(input_path, (str, bytes)):
            raise TypeError("each input path must be a valid file path")

        with open(input_path, "r", encoding="utf-8") as source:
            value = json.load(source)

        if not isinstance(value, dict):
            raise ValueError("each JSON file must contain a top-level object")

        merged.update(value)

    with open(output_path, "w", encoding="utf-8") as destination:
        json.dump(merged, destination, ensure_ascii=False)
        destination.write("\n")
