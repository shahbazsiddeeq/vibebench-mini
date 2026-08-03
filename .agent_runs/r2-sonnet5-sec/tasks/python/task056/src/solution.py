"""
Secure INI-style config parser.

Format:
    [section]
    key=value
    # comment
    (blank lines ignored)

parse_config(path) -> dict[str, dict[str, str]]
"""

import os
from typing import Dict


def parse_config(path: str) -> Dict[str, Dict[str, str]]:
    """Parse a simple INI-style config file.

    Args:
        path: path to the config file (str).

    Returns:
        dict mapping section name -> dict of key/value strings.

    Raises:
        TypeError: if path is not a string.
        FileNotFoundError: if the file does not exist.
        ValueError: on malformed content (duplicate sections,
            lines outside a section, malformed lines, empty
            section/key names).
    """
    if not isinstance(path, str):
        raise TypeError("path must be a string")

    if not path or "\x00" in path:
        raise ValueError("invalid path")

    # Normalize path; do not follow symlinks blindly beyond what os provides,
    # but we simply check existence and that it's a regular file.
    if not os.path.isfile(path):
        raise FileNotFoundError(f"config file not found: {path}")

    result: Dict[str, Dict[str, str]] = {}
    current_section = None

    try:
        with open(path, "r", encoding="utf-8", errors="strict") as f:
            lines = f.readlines()
    except OSError as exc:
        # Avoid leaking internal details; raise a generic error.
        raise ValueError("unable to read config file") from exc

    for lineno, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()

        if not line:
            continue
        if line.startswith("#"):
            continue

        if line.startswith("[") and line.endswith("]"):
            section_name = line[1:-1].strip()
            if not section_name:
                raise ValueError(f"empty section name at line {lineno}")
            if section_name in result:
                raise ValueError(f"duplicate section: {section_name}")
            result[section_name] = {}
            current_section = section_name
            continue

        if current_section is None:
            raise ValueError(f"key-value pair outside of section at line {lineno}")

        if "=" not in line:
            raise ValueError(f"malformed line (missing '='): {lineno}")

        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip()

        if not key:
            raise ValueError(f"empty key at line {lineno}")

        result[current_section][key] = value

    return result
