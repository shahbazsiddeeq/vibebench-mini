"""
src/solution.py

A simple, secure arithmetic expression tokenizer.

tokenize(expr) -> list

Splits an arithmetic expression string into a list of tokens:
- Numbers containing a '.' become Python float.
- Numbers without a '.' become Python int.
- Single-character operators/parentheses + - * / ( ) ^ % are emitted as str.
- Whitespace is ignored.
- Any other character raises ValueError.

This implementation avoids eval/exec and any dynamic code execution,
uses only the standard library, and carefully validates all input.
"""

from typing import List, Union

Token = Union[int, float, str]

_OPERATORS = set("+-*/()^%")
_DIGITS = set("0123456789")


def tokenize(expr: str) -> List[Token]:
    """
    Tokenize an arithmetic expression string.

    Args:
        expr: The expression string to tokenize.

    Returns:
        A list of tokens (int, float, or str).

    Raises:
        ValueError: If the input is not a string, or contains an
                    invalid character, or contains a malformed number.
    """
    if not isinstance(expr, str):
        raise ValueError("Expression must be a string")

    tokens: List[Token] = []
    i = 0
    n = len(expr)

    while i < n:
        ch = expr[i]

        if ch.isspace():
            i += 1
            continue

        if ch in _OPERATORS:
            tokens.append(ch)
            i += 1
            continue

        if ch in _DIGITS or ch == ".":
            start = i
            dot_count = 0
            while i < n and (expr[i] in _DIGITS or expr[i] == "."):
                if expr[i] == ".":
                    dot_count += 1
                    if dot_count > 1:
                        raise ValueError(
                            f"Malformed number near position {start}"
                        )
                i += 1
            num_str = expr[start:i]

            # Must contain at least one digit to be valid.
            if not any(c in _DIGITS for c in num_str):
                raise ValueError(f"Malformed number near position {start}")

            try:
                if "." in num_str:
                    tokens.append(float(num_str))
                else:
                    tokens.append(int(num_str))
            except (ValueError, OverflowError) as exc:
                raise ValueError(
                    f"Malformed number near position {start}"
                ) from exc
            continue

        # Any other character is invalid.
        raise ValueError(f"Invalid character encountered: {ch!r}")

    return tokens
