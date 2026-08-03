from __future__ import annotations

from pathlib import Path


def parse_config(path: str) -> dict[str, dict[str, str]]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"No such file: {path}")
    result: dict[str, dict[str, str]] = {}
    current_section: str | None = None
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            section = line[1:-1].strip()
            if section in result:
                raise ValueError(f"Duplicate section: {section}")
            result[section] = {}
            current_section = section
        elif "=" in line and current_section is not None:
            key, _, value = line.partition("=")
            result[current_section][key.strip()] = value.strip()
    return result
