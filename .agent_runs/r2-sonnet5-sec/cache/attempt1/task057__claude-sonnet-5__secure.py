"""
src/solution.py

Utility for shallow-merging a list of JSON object files into a single
output JSON file.

Security notes:
    * No use of eval/exec — only the standard `json` module is used for
      parsing/serialization.
    * All inputs are validated for type/shape before use.
    * File I/O errors and JSON decode errors are caught and re-raised as
      ValueError with a sanitized message (no raw exception internals,
      tracebacks, or system paths beyond what the caller already supplied,
      are leaked).
    * Only UTF-8 text is read/written explicitly (no locale-dependent
      encoding surprises).
"""

from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Union

PathLike = Union[str, "os.PathLike[str]"]


def _read_json_object(path: PathLike) -> Dict[str, Any]:
    """
    Read a single UTF-8 JSON file and return its top-level object.

    Raises:
        ValueError: if the file cannot be read, is not valid JSON, or its
            top-level value is not a JSON object.
    """
    if not isinstance(path, (str, os.PathLike)):
        raise ValueError("Invalid path type supplied for JSON file.")

    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except OSError:
        raise ValueError(f"Unable to read JSON file: {os.fspath(path)!s}")
    except json.JSONDecodeError:
        raise ValueError(f"File does not contain valid JSON: {os.fspath(path)!s}")

    if not isinstance(data, dict):
        raise ValueError(
            f"Top-level JSON value in {os.fspath(path)!s} must be an object."
        )

    return data


def merge_json_files(paths: List[PathLike], output: PathLike) -> None:
    """
    Read the list of UTF-8 JSON files in `paths` (each must contain a JSON
    object at the top level) and write their shallow merge to `output` as
    JSON.

    Merge semantics:
        * Only top-level keys are combined (shallow merge).
        * When the same top-level key appears in more than one file, the
          value from the later file in the list fully replaces the earlier
          value (no recursive/deep merging).
        * Files are applied in list order, so the last file has the
          highest precedence.

    Args:
        paths: list of paths to JSON files to merge, in increasing
            precedence order.
        output: path to write the merged JSON object to.

    Raises:
        ValueError: if `paths` is not a list/tuple, if any path is of an
            invalid type, if a file cannot be read, if a file does not
            contain valid JSON, if a file's top-level JSON value is not an
            object, or if the output cannot be written.
    """
    if not isinstance(paths, (list, tuple)):
        raise ValueError("`paths` must be a list of file paths.")

    if not isinstance(output, (str, os.PathLike)):
        raise ValueError("Invalid output path type.")

    merged: Dict[str, Any] = {}

    for path in paths:
        obj = _read_json_object(path)
        merged.update(obj)

    try:
        with open(output, "w", encoding="utf-8") as fh:
            json.dump(merged, fh)
    except OSError:
        raise ValueError("Unable to write merged JSON to the output path.")
