import string


def check_password(pw):
    length = len(pw)
    has_upper = any(c.isupper() for c in pw)
    has_lower = any(c.islower() for c in pw)
    has_digit = any(c.isdigit() for c in pw)
    has_special = any(c in string.punctuation for c in pw)

    score = sum([
        length >= 8,
        has_upper,
        has_lower,
        has_digit,
        has_special
    ])

    return {
        "length": length,
        "has_upper": has_upper,
        "has_lower": has_lower,
        "has_digit": has_digit,
        "has_special": has_special,
        "score": score
    }
