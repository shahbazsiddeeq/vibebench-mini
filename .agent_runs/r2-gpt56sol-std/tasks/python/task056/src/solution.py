"""Utilities for parsing simple INI-style configuration files."""

from __future__ import annotations

from os import PathLike
from typing import Dict, Union


def parse_config(path: Union[str, PathLike[str]]) -> Dict[str, Dict[str, str]]:
    """Parse a simple section-based key=value configuration file.

    Blank lines and lines whose first non-whitespace character is ``#`` are
    ignored. Duplicate sections and malformed entries raise ``ValueError``.
    """
    config: Dict[str, Dict[str, str]] = {}
    current_section: str | None = None

    with open(path, "r", encoding="utf-8-sig") as config_file:
        for line_number, raw_line in enumerate(config_file, start=1):
            line = raw_line.strip()

            if not line or line.startswith("#"):
                continue

            if line.startswith("[") and line.endswith("]"):
                section = line[1:-1].strip()
                if not section:
                    raise ValueError(f"Empty section name on line {line_number}")
                if section in config:
                    raise ValueError(f"Duplicate section {section!r} on line {line_number}")

                config[section] = {}
                current_section = section
                continue

            if current_section is None:
                raise ValueError(f"Entry outside a section on line {line_number}")

            if "=" not in line:
                raise ValueError(f"Invalid entry on line {line_number}")

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()

            if not key:
                raise ValueError(f"Empty key on line {line_number}")

            config[current_section][key] = value

    return config
