from __future__ import annotations

import re


def to_snake(s: str) -> str:
    s = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", s)
    s = re.sub(r"([a-z\d])([A-Z])", r"\1_\2", s)
    return s.lower()


def to_camel(s: str) -> str:
    parts = s.split("_")
    if not parts:
        return s
    return parts[0].lower() + "".join(p.capitalize() for p in parts[1:])
