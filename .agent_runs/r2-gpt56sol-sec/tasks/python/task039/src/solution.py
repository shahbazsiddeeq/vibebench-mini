"""Run-length encoding and decoding utilities."""

from __future__ import annotations

import sys


def _validate_string(value: object, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    return value


def _is_ascii_digit(character: str) -> bool:
    return "0" <= character <= "9"


def rle_encode(s: str) -> str:
    """Encode consecutive character runs as a decimal count and character."""
    s = _validate_string(s, "s")
    if not s:
        return ""

    if any(_is_ascii_digit(character) for character in s):
        raise ValueError("input must not contain ASCII digits")

    encoded: list[str] = []
    run_character = s[0]
    run_length = 1

    for character in s[1:]:
        if character == run_character:
            run_length += 1
        else:
            encoded.append(str(run_length))
            encoded.append(run_character)
            run_character = character
            run_length = 1

    encoded.append(str(run_length))
    encoded.append(run_character)
    return "".join(encoded)


def rle_decode(s: str) -> str:
    """Decode a run-length encoded string.

    Valid tokens consist of one or more ASCII digits representing a non-zero
    count, followed by one non-ASCII-digit character.
    """
    s = _validate_string(s, "s")
    if not s:
        return ""

    decoded: list[str] = []
    total_length = 0
    index = 0
    input_length = len(s)

    while index < input_length:
        if not _is_ascii_digit(s[index]):
            raise ValueError("malformed run-length encoding")

        count = 0
        while index < input_length and _is_ascii_digit(s[index]):
            digit = ord(s[index]) - ord("0")
            if count > (sys.maxsize - digit) // 10:
                raise ValueError("decoded output is too large")
            count = count * 10 + digit
            index += 1

        if count == 0 or index >= input_length:
            raise ValueError("malformed run-length encoding")

        character = s[index]
        if _is_ascii_digit(character):
            raise ValueError("malformed run-length encoding")
        index += 1

        if count > sys.maxsize - total_length:
            raise ValueError("decoded output is too large")
        total_length += count

        try:
            decoded.append(character * count)
        except (MemoryError, OverflowError) as exc:
            raise ValueError("decoded output is too large") from exc

    try:
        return "".join(decoded)
    except (MemoryError, OverflowError) as exc:
        raise ValueError("decoded output is too large") from exc


__all__ = ["rle_encode", "rle_decode"]
