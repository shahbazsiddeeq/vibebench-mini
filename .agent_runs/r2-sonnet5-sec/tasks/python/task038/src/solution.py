"""
Caesar Cipher implementation.

Provides a single public function, ``caesar``, which shifts alphabetic
characters in a string by a given amount while preserving case and
leaving non-alphabetic characters untouched.
"""

from __future__ import annotations

_ALPHABET_SIZE = 26
_LOWER_A = ord("a")
_UPPER_A = ord("A")


def caesar(text: str, shift: int) -> str:
    """
    Shift alphabetic characters in ``text`` by ``shift`` positions.

    - Case is preserved (uppercase stays uppercase, lowercase stays lowercase).
    - Non-alphabetic characters are left unchanged.
    - ``shift`` may be any integer (positive, negative, or larger than 26);
      it is normalized modulo 26.

    Parameters
    ----------
    text : str
        The input text to encode/decode.
    shift : int
        The number of positions to shift each letter.

    Returns
    -------
    str
        The resulting text after applying the Caesar cipher.

    Raises
    ------
    TypeError
        If ``text`` is not a ``str`` or ``shift`` is not an ``int``.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if isinstance(shift, bool) or not isinstance(shift, int):
        # bool is a subclass of int; explicitly reject to avoid surprises.
        raise TypeError("shift must be an integer")

    normalized_shift = shift % _ALPHABET_SIZE

    result_chars = []
    for char in text:
        if "a" <= char <= "z":
            base = _LOWER_A
        elif "A" <= char <= "Z":
            base = _UPPER_A
        else:
            result_chars.append(char)
            continue

        offset = (ord(char) - base + normalized_shift) % _ALPHABET_SIZE
        result_chars.append(chr(base + offset))

    return "".join(result_chars)
