from __future__ import annotations

import os
from collections.abc import Mapping


def write_config(
    path: str | os.PathLike[str],
    config: Mapping[str, Mapping[str, str]],
) -> None:
    sections: list[str] = []

    for section, entries in config.items():
        lines = [f"[{section}]"]
        for key, value in entries.items():
            if "\n" in value or "\r" in value:
                raise ValueError("configuration values must not contain line breaks")
            lines.append(f"{key}={value}")
        sections.append("\n".join(lines))

    content = "\n\n".join(sections)
    if sections:
        content += "\n"

    with open(path, "w", encoding="utf-8", newline="\n") as file:
        file.write(content)
