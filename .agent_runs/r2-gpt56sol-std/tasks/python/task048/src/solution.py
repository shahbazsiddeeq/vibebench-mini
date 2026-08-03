"""Password strength checking utilities."""

import string


def check_password(pw: str) -> dict:
    """Return password length, character-class flags, and strength score."""
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
