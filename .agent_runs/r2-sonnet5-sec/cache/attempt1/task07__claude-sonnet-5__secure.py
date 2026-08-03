"""
Email Masker
============

Provides `mask_email`, a function that scans a block of text for email
addresses and masks the "username" portion (the part before the ``@``)
while leaving the domain portion untouched.

Design notes / security considerations:
    * Only the standard library is used (``re``).
    * The regular expression used to detect e-mail-like tokens is
      intentionally conservative and bounded (no nested quantifiers,
      no catastrophic backtracking patterns) to avoid ReDoS issues.
    * The function never executes or evaluates any part of the input;
      it purely performs pattern matching and string substitution.
    * Input is validated to be a string; a clear, non-leaky error is
      raised otherwise (no internal state or stack traces exposed).
"""

import re

# Pattern for a "username" (local-part) made of common, safe characters.
_USERNAME_CHARS = r"[A-Za-z0-9._%+-]+"

# Pattern for a domain: letters/digits/hyphens/dots, must start and end
# with an alphanumeric character. This covers both "example.com" and
# bare hosts like "localhost".
_DOMAIN_CHARS = r"[A-Za-z0-9](?:[A-Za-z0-9.-]*[A-Za-z0-9])?"

_EMAIL_RE = re.compile(rf"(?P<user>{_USERNAME_CHARS})@(?P<domain>{_DOMAIN_CHARS})")


def _mask_match(match: "re.Match") -> str:
    """Given a regex match for an email address, return the masked form."""
    user = match.group("user")
    domain = match.group("domain")

    first = user[0]
    last = user[-1] if len(user) > 1 else user[0]

    return f"{first}***{last}@{domain}"


def mask_email(s: str) -> str:
    """
    Find email addresses in ``s`` and mask the username portion.

    The username (part before ``@``) is replaced with its first
    character, then ``***``, then its last character. For a
    single-character username, the same character is used for both
    first and last. The domain (part after ``@``) is left unchanged,
    including its case. Text that is not part of an email address is
    left unchanged.

    :param s: The input text to scan.
    :return: The text with any detected email addresses masked.
    :raises TypeError: If ``s`` is not a string.
    """
    if not isinstance(s, str):
        raise TypeError("mask_email expects a string input")

    return _EMAIL_RE.sub(_mask_match, s)
