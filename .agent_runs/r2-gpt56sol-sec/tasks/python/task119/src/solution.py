"""Arithmetic expression tokenizer."""

from typing import Union

Token = Union[int, float, str]

_OPERATORS = frozenset("+-*/()^%")
_DIGITS = frozenset("0123456789")


def tokenize(expr: str) -> list[Token]:
    """Split an arithmetic expression into numbers and operator tokens.

    Integer literals become ``int`` objects, decimal literals become
    ``float`` objects, whitespace is ignored, and unsupported characters or
    malformed numbers raise ``ValueError``.
    """
    if not isinstance(expr, str):
        raise TypeError("expr must be a string")

    tokens: list[Token] = []
    index = 0

    while index < len(expr):
        char = expr[index]

        if char.isspace():
            index += 1
            continue

        if char in _OPERATORS:
            tokens.append(char)
            index += 1
            continue

        if char in _DIGITS or char == ".":
            start = index
            dot_count = 0
            digit_count = 0

            while index < len(expr):
                current = expr[index]
                if current in _DIGITS:
                    digit_count += 1
                    index += 1
                elif current == ".":
                    dot_count += 1
                    index += 1
                else:
                    break

            literal = expr[start:index]
            if digit_count == 0 or dot_count > 1:
                raise ValueError("invalid numeric literal")

            try:
                value: Union[int, float]
                value = float(literal) if dot_count == 1 else int(literal)
            except (ValueError, OverflowError):
                raise ValueError("invalid numeric literal") from None

            tokens.append(value)
            continue

        raise ValueError("invalid character in expression")

    return tokens
