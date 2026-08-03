"""Utilities for parsing simple INI-style configuration files."""

from __future__ import annotations

import os
from typing import Dict, Union

PathType = Union[str, bytes, os.PathLike[str], os.PathLike[bytes]]


def parse_config(path: PathType) -> Dict[str, Dict[str, str]]:
    """Parse a simple section-based ``key=value`` configuration file.

    Blank lines and lines whose first non-whitespace character is ``#`` are
    ignored. Section names and keys must be non-empty. Duplicate sections,
    duplicate keys, malformed lines, and entries outside a section raise
    ``ValueError``.
    """
    if not isinstance(path, (str, bytes, os.PathLike)):
        raise TypeError("path must be a string, bytes, or path-like object")

    result: Dict[str, Dict[str, str]] = {}
    current_section: str | None = None

    with open(path, "r", encoding="utf-8") as config_file:
        for line_number, raw_line in enumerate(config_file, start=1):
            line = raw_line.strip()

            if not line or line.startswith("#"):
                continue

            if line.startswith("["):
                if not line.endswith("]"):
                    raise ValueError(f"malformed section header on line {line_number}")

                section = line[1:-1].strip()
                if not section or "[" in section or "]" in section:
                    raise ValueError(f"invalid section name on line {line_number}")
                if section in result:
                    raise ValueError(f"duplicate section on line {line_number}")

                result[section] = {}
                current_section = section
                continue

            if current_section is None:
                raise ValueError(f"entry outside a section on line {line_number}")
            if "=" not in line:
                raise ValueError(f"malformed entry on line {line_number}")

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()

            if not key:
                raise ValueError(f"empty key on line {line_number}")
            if key in result[current_section]:
                raise ValueError(f"duplicate key on line {line_number}")

            result[current_section][key] = value

    return result


__all__ = ["parse_config"]
