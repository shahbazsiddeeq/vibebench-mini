"""Password strength checking utilities."""

import string
from typing import Dict, Union


def check_password(pw: str) -> Dict[str, Union[int, bool]]:
    """Return password strength criteria and a score from 0 to 5."""
    if not isinstance(pw, str):
        raise TypeError("pw must be a string")

    length = len(pw)
    has_upper = any(char.isupper() for char in pw)
    has_lower = any(char.islower() for char in pw)
    has_digit = any(char.isdigit() for char in pw)
    has_special = any(char in string.punctuation for char in pw)

    score = sum(
        (
            length >= 8,
            has_upper,
            has_lower,
            has_digit,
            has_special,
        )
    )

    return {
        "length": length,
        "has_upper": has_upper,
        "has_lower": has_lower,
        "has_digit": has_digit,
        "has_special": has_special,
        "score": score,
    }
