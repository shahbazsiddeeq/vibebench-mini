from __future__ import annotations

import re


def find_replace(text: str, replacements: dict[str, str]) -> str:
    if not replacements:
        return text
    # Sort by length descending so longer keys match first
    pattern = re.compile(
        "|".join(re.escape(k) for k in sorted(replacements, key=len, reverse=True))
    )
    return pattern.sub(lambda m: replacements[m.group(0)], text)
