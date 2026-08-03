from __future__ import annotations

import string


def check_password(pw: str) -> dict:
    has_upper = any(c.isupper() for c in pw)
    has_lower = any(c.islower() for c in pw)
    has_digit = any(c.isdigit() for c in pw)
    has_special = any(c in string.punctuation for c in pw)
    long_enough = len(pw) >= 8
    score = sum([has_upper, has_lower, has_digit, has_special, long_enough])
    return {
        "length": len(pw),
        "has_upper": has_upper,
        "has_lower": has_lower,
        "has_digit": has_digit,
        "has_special": has_special,
        "score": score,
    }
