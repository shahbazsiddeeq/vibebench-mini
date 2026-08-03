"""Utilities for masking email addresses in text."""

from __future__ import annotations

import re
from typing import Match


_LOCAL_CHARS = r"A-Za-z0-9._%+\-"
_DOMAIN_LABEL = r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"

_EMAIL_PATTERN = re.compile(
    rf"""
    (?<![{_LOCAL_CHARS}@])
    (?P<username>
        [A-Za-z0-9]
        (?:[{_LOCAL_CHARS}]*[A-Za-z0-9])?
    )
    @
    (?P<domain>
        {_DOMAIN_LABEL}
        (?:\.{_DOMAIN_LABEL})*
    )
    (?![A-Za-z0-9_-])
    """,
    re.VERBOSE,
)


def mask_email(s: str) -> str:
    """Mask usernames in email addresses found within *s*.

    The domain is preserved exactly. A username is replaced by its first
    character, three asterisks, and its last character.
    """
    if not isinstance(s, str):
        raise TypeError("s must be a string")

    def replace(match: Match[str]) -> str:
        username = match.group("username")
        domain = match.group("domain")
        return f"{username[0]}***{username[-1]}@{domain}"

    return _EMAIL_PATTERN.sub(replace, s)
