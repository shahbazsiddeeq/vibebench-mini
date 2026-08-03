"""Simultaneous find-and-replace utilities."""

import re
from collections.abc import Mapping


def find_replace(text: str, replacements: Mapping[str, str]) -> str:
    """Apply replacements simultaneously, preferring longer matching keys."""
    if not replacements:
        return text

    keys = sorted(replacements, key=len, reverse=True)
    pattern = re.compile("|".join(re.escape(key) for key in keys))
    return pattern.sub(lambda match: replacements[match.group(0)], text)
