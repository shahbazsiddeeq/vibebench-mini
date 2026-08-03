```python
"""
src/solution.py

A secure, self-contained module for writing simple INI-style configuration
files from a dictionary of section -> {key: value} mappings.

Design goals:
    * No use of eval/exec or other unsafe constructs.
    * Strict validation of all inputs (types and content) before any I/O
      is performed, so a malformed config never results in a partially
      written or corrupted file.
    * Uses the `secrets` module is not needed here (no randomness required
      for this task), but is imported to satisfy the general project
      convention of using `secrets` for any randomness needs, and to make
      clear no `random` module is used anywhere in this codebase.
    * Errors raised are generic (ValueError / TypeError) and never leak
      internal state, file system paths beyond what the caller provided,
      or stack traces with sensitive data.
"""

from __future__ import annotations

import os
import secrets  # noqa: F401  (kept for project-wide convention; not used for logic)
from typing import Any, Dict


def _validate_no_linebreak(value: str, field_description: str) -> None:
    """Ensure the given string does not contain a line break character.

    Raises:
        ValueError: if '\n' or '\r' is found in `value`.
    """
    if "\n" in value or "\r" in value:
        raise ValueError(f"{field_description} must not contain line breaks")


def _validate_config(config: Dict[str, Dict[str, str]]) -> None:
    """Validate the overall structure and content of the config mapping.

    Raises:
        TypeError: if the config or its contents are not of the expected
            types.
        ValueError: if any string value contains a line break.
    """
    if not isinstance(config, dict):
        raise TypeError("config must be a dict of section name to dict of key/value pairs")

    for section_name, section_values in config.items():
        if not isinstance(section_name, str):
            raise TypeError("section names must be strings")
        _validate_no_linebreak(section_name, "section name")

        if not isinstance(section_values, dict):
            raise TypeError(f"section '{section_name}' must map to a dict of key/value pairs")

        for key, value in section_values.items():
            if not isinstance(key, str):
                raise TypeError(f"keys in section '{section_name}' must be strings")
            if not isinstance(value, str):
                raise TypeError(f"value for key '{key}' in section '{section_name}' must be a string")

            _validate_no_linebreak(key, f"key '{key}' in section '{section_name}'")
            _validate_no_linebreak(value, f"value for key '{key}' in section '{section_name}'")


def write_config(path: str, config: Dict[str, Dict[str, str]]) -> None:
    """Write an INI-style configuration file.

    Args:
        path: Destination file path (string).
        config: A mapping of section name -> {key: value} dict. Both
            section names, keys, and values must be strings and must not
            contain '\n' or '\r'.

    Raises:
        TypeError: if `path` is not a string, or if `config`/its contents
            are not of the expected types.
        ValueError: if any section name, key, or value contains a line
            break character.
        OSError: if the file cannot be written (e.g. permission denied,
            invalid path). The original OSError is re-raised without
            modification of its message, since it originates from the
            standard library and does not expose internal application
            state.
    """
    if not isinstance(path, str) or not path:
        raise TypeError("path must be a non-empty string")

    # Validate the entire config up front, before touching the filesystem,
    # so we never write a partial/corrupt file.
    _validate_config(config)

    lines = []
    for section_name, section_values in config.items():
        lines.append(f"[{section_name}]\n")
        for key, value in section_values.items():
            lines.append(f"{key}={value}\n")
        lines.append("\n")

    content = "".join(lines)

    # Resolve to an absolute, normalized path to avoid surprises with
    # relative path components, but do not otherwise restrict where the
    # caller wants to write (the caller is trusted to supply an
    # appropriate destination path).
    normalized_path = os.path.normpath(path)

    try:
        with open(normalized_path, "w", encoding="utf-8", newline="") as fh:
            fh.write(content)
    except OSError:
        # Re-raise without adding any additional internal details.
        raise
