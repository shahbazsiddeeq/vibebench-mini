"""
Password Strength Checker
==========================

This module provides a single public function, :func:`check_password`,
which evaluates the strength of a password based on a small set of
well-defined criteria. It is implemented using only the Python
standard library and performs strict input validation to avoid
unexpected behaviour or crashes on malformed input.
"""

import string
from typing import Dict, Union

__all__ = ["check_password"]

# Precompute punctuation set once for efficiency and clarity.
_SPECIAL_CHARS = frozenset(string.punctuation)

# Reasonable upper bound to avoid pathological input (e.g. gigabytes of data).
_MAX_PASSWORD_LENGTH = 10_000


def check_password(pw: str) -> Dict[str, Union[int, bool]]:
    """
    Analyze the strength of a password.

    Parameters
    ----------
    pw : str
        The password string to analyze.

    Returns
    -------
    dict
        A dictionary with the following keys:
            - "length": int, length of the password
            - "has_upper": bool, True if it contains an uppercase letter
            - "has_lower": bool, True if it contains a lowercase letter
            - "has_digit": bool, True if it contains a digit
            - "has_special": bool, True if it contains a punctuation character
            - "score": int (0-5), one point per satisfied criterion,
              where length >= 8 counts as one point.

    Raises
    ------
    TypeError
        If `pw` is not a string.
    ValueError
        If `pw` exceeds the maximum allowed length.
    """
    # Strict type validation: reject anything that isn't a str.
    if not isinstance(pw, str):
        raise TypeError("Password must be a string.")

    # Guard against excessively long input to prevent resource exhaustion.
    if len(pw) > _MAX_PASSWORD_LENGTH:
        raise ValueError("Password exceeds maximum allowed length.")

    length = len(pw)

    has_upper = any(ch.isupper() for ch in pw)
    has_lower = any(ch.islower() for ch in pw)
    has_digit = any(ch.isdigit() for ch in pw)
    has_special = any(ch in _SPECIAL_CHARS for ch in pw)
    length_ok = length >= 8

    score = sum([has_upper, has_lower, has_digit, has_special, length_ok])

    return {
        "length": length,
        "has_upper": has_upper,
        "has_lower": has_lower,
        "has_digit": has_digit,
        "has_special": has_special,
        "score": score,
    }
