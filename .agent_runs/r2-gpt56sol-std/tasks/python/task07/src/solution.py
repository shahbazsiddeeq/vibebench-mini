"""Utilities for masking email addresses in text."""

import re
from typing import Match

__all__ = ["mask_email"]

_LOCAL = r"[A-Za-z0-9](?:[A-Za-z0-9._%+'-]*[A-Za-z0-9])?"
_LABEL = r"[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?"
_DOMAIN = rf"{_LABEL}(?:\.{_LABEL})*"

_EMAIL_RE = re.compile(
    rf"(?<![A-Za-z0-9._%+'-])(?P<username>{_LOCAL})@(?P<domain>{_DOMAIN})"
    rf"(?![A-Za-z0-9_-])"
)


def mask_email(s: str) -> str:
    """Mask usernames in email addresses found within *s*."""

    def replace(match: Match[str]) -> str:
        username = match.group("username")
        domain = match.group("domain")
        return f"{username[0]}***{username[-1]}@{domain}"

    return _EMAIL_RE.sub(replace, s)
