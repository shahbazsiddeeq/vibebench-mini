"""Utilities for creating ASCII URL slugs."""

import re
import unicodedata


_NON_ALNUM_RUN = re.compile(r"[^a-z0-9]+")


def slugify(s: str) -> str:
    """Return a lowercase ASCII slug derived from *s*."""
    if not isinstance(s, str):
        raise TypeError("slugify() requires a string")

    normalized = unicodedata.normalize("NFKD", s)
    ascii_text = normalized.encode("ascii", errors="ignore").decode("ascii")
    return _NON_ALNUM_RUN.sub("-", ascii_text.lower()).strip("-")
