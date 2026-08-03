"""
src/solution.py

A secure, self-contained module implementing an integer-to-base string
converter.

Security considerations:
- Strict input validation (type and value checks) for all public inputs.
- No use of eval/exec or any dynamic code execution.
- No I/O operations (no file, network, or print side-effects).
- No use of non-deterministic or insecure randomness (none needed here,
  but if any randomness were required, `secrets` would be used per
  project policy).
- Errors are raised with clear, non-sensitive messages (no internal
  state, stack traces, or system details are exposed).
"""

from typing import Union

# Digits used for bases up to 36: 0-9 followed by a-z (lowercase, as per spec)
_DIGITS = "0123456789abcdefghijklmnopqrstuvwxyz"

_MIN_BASE = 2
_MAX_BASE = 36


def int_to_base(n: Union[int, bool], base: Union[int, bool]) -> str:
    """
    Convert a non-negative integer `n` into its string representation in
    the given `base` (between 2 and 36, inclusive).

    Digits 0-9 are used first, followed by lowercase letters a-z for
    values above 9.

    Args:
        n: A non-negative integer to convert.
        base: The base to convert to, must be in [2, 36].

    Returns:
        The string representation of `n` in the specified base.

    Raises:
        ValueError: If `n` is negative, or `base` is out of [2, 36],
                    or if inputs are not valid integers.
    """
    # Reject bool explicitly, since bool is a subclass of int in Python
    # and could lead to confusing/unexpected behavior if silently accepted.
    if isinstance(n, bool) or not isinstance(n, int):
        raise ValueError("n must be an integer")

    if isinstance(base, bool) or not isinstance(base, int):
        raise ValueError("base must be an integer")

    if n < 0:
        raise ValueError("n must be a non-negative integer")

    if base < _MIN_BASE or base > _MAX_BASE:
        raise ValueError(f"base must be between {_MIN_BASE} and {_MAX_BASE}")

    if n == 0:
        return "0"

    digits = []
    value = n
    while value > 0:
        value, remainder = divmod(value, base)
        digits.append(_DIGITS[remainder])

    digits.reverse()
    return "".join(digits)
