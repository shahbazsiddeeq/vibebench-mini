"""Utilities for writing INI-style configuration files."""

from __future__ import annotations

import os
from collections.abc import Mapping
from typing import Union

PathType = Union[str, bytes, os.PathLike[str], os.PathLike[bytes]]


def write_config(path: PathType, config: Mapping[str, Mapping[str, str]]) -> None:
    """Write *config* to *path* in INI-style format using UTF-8 encoding."""
    if not isinstance(path, (str, bytes, os.PathLike)):
        raise TypeError("path must be a string or path-like object")
    if not isinstance(config, Mapping):
        raise TypeError("config must be a mapping")

    lines: list[str] = []

    for section, entries in config.items():
        if not isinstance(section, str):
            raise TypeError("section names must be strings")
        if "\n" in section or "\r" in section:
            raise ValueError("section names must not contain line breaks")
        if not isinstance(entries, Mapping):
            raise TypeError("each section must contain a mapping")

        lines.append(f"[{section}]\n")

        for key, value in entries.items():
            if not isinstance(key, str):
                raise TypeError("configuration keys must be strings")
            if not isinstance(value, str):
                raise TypeError("configuration values must be strings")
            if "\n" in key or "\r" in key:
                raise ValueError("configuration keys must not contain line breaks")
            if "\n" in value or "\r" in value:
                raise ValueError("configuration values must not contain line breaks")

            lines.append(f"{key}={value}\n")

        lines.append("\n")

    with open(path, "w", encoding="utf-8", newline="\n") as config_file:
        config_file.write("".join(lines))
