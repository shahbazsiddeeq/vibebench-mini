"""
src/solution.py

Safe YAML -> canonical JSON conversion utility.

Security considerations:
- Uses yaml.safe_load exclusively; never yaml.load with a permissive loader.
- Custom/unsafe tags (e.g. !!python/object/apply:...) will raise yaml.YAMLError
  because the SafeLoader has no constructor for them.
- Input path is validated to be a string/os.PathLike; file is opened explicitly
  as UTF-8 text, and any I/O or parsing errors are wrapped into clear,
  non-leaking exceptions.
- No eval/exec, no dynamic code execution.
"""

import datetime
import json
import os
from typing import Any

import yaml


def _default_serializer(obj: Any) -> str:
    """
    Fallback serializer for json.dumps to handle objects that have no
    native JSON representation (e.g. datetime.date, datetime.datetime,
    datetime.time). These are converted to their string form.
    """
    if isinstance(obj, (datetime.date, datetime.datetime, datetime.time)):
        return obj.isoformat() if False else str(obj)
    # Fallback: use str() representation for anything else unsupported.
    return str(obj)


def yaml_to_json(path: str) -> str:
    """
    Read a UTF-8 YAML file at `path` using PyYAML's safe loader and return
    a canonical JSON string.

    Canonicalization rules:
      - Keys are sorted (sort_keys=True).
      - Compact separators: "," and ":" (no spaces).
      - Non-ASCII characters are emitted as-is (ensure_ascii=False).
      - Values without a native JSON representation (e.g. YAML dates) are
        serialized as their string form.
      - An empty YAML file (parses to None) produces the JSON string "null".

    Raises:
      - TypeError: if `path` is not a string or os.PathLike.
      - FileNotFoundError: if the file does not exist.
      - yaml.YAMLError: if the YAML content is invalid or contains unsafe
        constructs that safe_load refuses to build.
      - ValueError: for other unexpected failures, without leaking internal
        details.
    """
    if not isinstance(path, (str, os.PathLike)):
        raise TypeError("path must be a string or os.PathLike")

    # Normalize to a string path for consistent error handling.
    file_path = os.fspath(path)

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"No such file: {file_path!r}")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError as exc:
        raise ValueError("File is not valid UTF-8 text") from exc
    except OSError as exc:
        raise ValueError("Unable to read the specified file") from exc

    try:
        data = yaml.safe_load(content)
    except yaml.YAMLError:
        # Propagate YAML-specific errors (including unsafe tag rejections)
        # directly, as required by the contract.
        raise
    except Exception as exc:
        # Wrap any unexpected loader failure without exposing internals.
        raise ValueError("Failed to parse YAML content") from exc

    try:
        return json.dumps(
            data,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            default=_default_serializer,
        )
    except (TypeError, ValueError) as exc:
        raise ValueError("Failed to serialize parsed YAML content to JSON") from exc
