"""
Run-Length Encoding utilities.

This module provides two functions:

- ``rle_encode(s)``: Encode a string using run-length encoding, where each
  run of identical characters is represented as ``<count><char>``.
- ``rle_decode(s)``: Decode a run-length encoded string back to its
  original form.

Both functions perform strict input validation and raise ``ValueError``
on malformed or ambiguous input. No external I/O, ``eval``/``exec``, or
non-standard-library dependencies are used.
"""

from __future__ import annotations

import re

# Precompiled pattern used to find a leading run of digits.
_DIGIT_RUN_RE = re.compile(r"\d+")


def rle_encode(s: str) -> str:
    """
    Encode ``s`` using run-length encoding.

    Each maximal run of identical consecutive characters is replaced by
    the run length followed by the character, e.g. ``"aaabbc"`` becomes
    ``"3a2b1c"``.

    :param s: The string to encode. Must not contain any ASCII digit
        (0-9), since digits are reserved for encoding counts and their
        presence would make the encoding ambiguous.
    :raises TypeError: If ``s`` is not a ``str``.
    :raises ValueError: If ``s`` contains any ASCII digit character.
    :return: The run-length encoded string.
    """
    if not isinstance(s, str):
        raise TypeError("Input must be a string")

    if any(ch.isdigit() for ch in s):
        raise ValueError("Input must not contain digit characters (0-9)")

    if s == "":
        return ""

    result: list[str] = []
    prev_char = s[0]
    count = 1

    for ch in s[1:]:
        if ch == prev_char:
            count += 1
        else:
            result.append(f"{count}{prev_char}")
            prev_char = ch
            count = 1

    result.append(f"{count}{prev_char}")
    return "".join(result)


def rle_decode(s: str) -> str:
    """
    Decode a run-length encoded string produced by :func:`rle_encode`.

    A valid encoded string is a concatenation of zero or more tokens,
    where each token consists of one or more digit characters (the
    count, which must not have a value of zero) followed by exactly one
    non-digit character.

    :param s: The run-length encoded string to decode.
    :raises TypeError: If ``s`` is not a ``str``.
    :raises ValueError: If ``s`` is malformed (e.g. missing count,
        missing character following a count, or a zero count).
    :return: The decoded string.
    """
    if not isinstance(s, str):
        raise TypeError("Input must be a string")

    if s == "":
        return ""

    result: list[str] = []
    pos = 0
    length = len(s)

    while pos < length:
        match = _DIGIT_RUN_RE.match(s, pos)
        if not match:
            raise ValueError(
                "Malformed input: expected a digit count at position "
                f"{pos}"
            )

        count_str = match.group()
        pos = match.end()

        if pos >= length:
            raise ValueError(
                "Malformed input: count is not followed by a character"
            )

        char = s[pos]
        pos += 1

        # This should be unreachable because _DIGIT_RUN_RE is greedy and
        # would have consumed any further digits, but we check defensively.
        if char.isdigit():
            raise ValueError("Malformed input: unexpected digit character")

        count = int(count_str)
        if count == 0:
            raise ValueError("Malformed input: count must be non-zero")

        result.append(char * count)

    return "".join(result)
