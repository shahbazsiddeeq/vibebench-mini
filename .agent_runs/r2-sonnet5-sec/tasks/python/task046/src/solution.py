"""
Morse Code Encoder
===================

This module provides a single public function, :func:`to_morse`, which
converts text containing letters (A-Z, case-insensitive) and digits
(0-9) into International Morse Code.

Design notes / security considerations:
- No use of eval/exec or dynamic code execution.
- No file, network, or subprocess I/O.
- Strict input validation: only ``str`` input is accepted; any other
  type raises ``TypeError``.
- Any character that is not an ASCII letter, digit, or whitespace
  raises ``ValueError`` (fails closed rather than silently ignoring
  unexpected input).
- Error messages are generic and do not leak internal state or stack
  traces.
"""

from __future__ import annotations

__all__ = ["to_morse"]

# Immutable mapping of supported characters to their Morse code
# representation. Defined as a tuple of pairs and converted to a dict
# to make accidental mutation slightly less likely, though the module
# does not expose this table publicly.
_MORSE_PAIRS = (
    ("A", ".-"), ("B", "-..."), ("C", "-.-."), ("D", "-.."), ("E", "."),
    ("F", "..-."), ("G", "--."), ("H", "...."), ("I", ".."), ("J", ".---"),
    ("K", "-.-"), ("L", ".-.."), ("M", "--"), ("N", "-."), ("O", "---"),
    ("P", ".--."), ("Q", "--.-"), ("R", ".-."), ("S", "..."), ("T", "-"),
    ("U", "..-"), ("V", "...-"), ("W", ".--"), ("X", "-..-"),
    ("Y", "-.--"), ("Z", "--.."),
    ("0", "-----"), ("1", ".----"), ("2", "..---"), ("3", "...--"),
    ("4", "....-"), ("5", "....."), ("6", "-...."), ("7", "--..."),
    ("8", "---.."), ("9", "----."),
)

_MORSE_TABLE = dict(_MORSE_PAIRS)


def to_morse(text: str) -> str:
    """Encode ``text`` into International Morse Code.

    Rules:
        - Case-insensitive: letters a-z / A-Z map identically.
        - Digits 0-9 are supported.
        - Letters within a word are separated by a single space.
        - Words (split on any whitespace) are separated by ``" / "``.
        - Any character that is not a letter, digit, or whitespace
          raises ``ValueError``.

    Args:
        text: The input string to encode.

    Returns:
        The Morse code representation of ``text``.

    Raises:
        TypeError: If ``text`` is not a ``str``.
        ValueError: If ``text`` contains a character that is not a
            letter, digit, or whitespace.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    # Validate every character up front so we fail fast and do not
    # partially process invalid input.
    for ch in text:
        if not (ch.isalpha() or ch.isdigit() or ch.isspace()):
            raise ValueError("text contains unsupported characters")
        if ch.isalpha() and ch.upper() not in _MORSE_TABLE:
            # Guards against non-ASCII "alpha" characters (e.g. accented
            # letters) which Python considers alphabetic but which are
            # not part of the supported A-Z table.
            raise ValueError("text contains unsupported characters")
        if ch.isdigit() and ch not in _MORSE_TABLE:
            # Guards against non-ASCII digit characters.
            raise ValueError("text contains unsupported characters")

    words = text.split()

    encoded_words = []
    for word in words:
        letters = [_MORSE_TABLE[ch.upper()] for ch in word]
        encoded_words.append(" ".join(letters))

    return " / ".join(encoded_words)
