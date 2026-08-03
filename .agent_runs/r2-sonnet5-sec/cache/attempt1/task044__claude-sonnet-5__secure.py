"""
solution.py
============

A small, dependency-free utility module providing two pure functions:

* ``to_snake(s)``  -- convert camelCase (or PascalCase) strings to snake_case.
* ``to_camel(s)``  -- convert snake_case strings to camelCase.

The implementation only relies on the Python standard library (``re``) and
performs strict input validation to avoid surprising behaviour or leaking
internal state through exception messages.
"""

from __future__ import annotations

import re

__all__ = ["to_snake", "to_camel"]

# Precompiled regular expressions used by ``to_snake``.
# 1) Insert an underscore before a capital-letter "word" that follows some
#    other character, e.g. "parseHTML" -> keeps acronym together but splits
#    a new capitalised word: "HTMLParser" -> "HTML_Parser".
_ACRONYM_BOUNDARY = re.compile(r"(.)([A-Z][a-z]+)")

# 2) Insert an underscore between a lowercase letter/digit and a following
#    uppercase letter, e.g. "parseHTML" -> "parse_HTML".
_CAMEL_BOUNDARY = re.compile(r"([a-z0-9])([A-Z])")


def _validate_string(value: object, name: str) -> str:
    """Validate that ``value`` is a ``str`` and return it.

    Raises:
        TypeError: if ``value`` is not a string.
    """
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    return value


def to_snake(s: str) -> str:
    """Convert a camelCase / PascalCase string to snake_case.

    Consecutive uppercase letters (an acronym) are kept together; only the
    final capital that starts a new lowercase word is split off.

    Examples:
        >>> to_snake("myVariableName")
        'my_variable_name'
        >>> to_snake("parseHTML")
        'parse_html'
        >>> to_snake("HTMLParser")
        'html_parser'
    """
    text = _validate_string(s, "s")

    # Guard against pathologically large input to avoid excessive resource
    # consumption from a hostile caller.
    if len(text) > 10_000:
        raise ValueError("input string is too long")

    step1 = _ACRONYM_BOUNDARY.sub(r"\1_\2", text)
    step2 = _CAMEL_BOUNDARY.sub(r"\1_\2", step1)
    return step2.lower()


def to_camel(s: str) -> str:
    """Convert a snake_case string to camelCase.

    The first letter of the output is always lowercase; the first letter of
    every subsequent underscore-separated part is capitalised.

    Examples:
        >>> to_camel("my_variable_name")
        'myVariableName'
        >>> to_camel("my_var")
        'myVar'
    """
    text = _validate_string(s, "s")

    if len(text) > 10_000:
        raise ValueError("input string is too long")

    parts = [p for p in text.split("_") if p != ""]

    if not parts:
        return ""

    first = parts[0].lower()
    rest = "".join(part[:1].upper() + part[1:].lower() for part in parts[1:])
    return first + rest
