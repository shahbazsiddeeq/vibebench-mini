from __future__ import annotations


def validate_isbn13(isbn: str) -> bool:
    clean = isbn.replace("-", "").replace(" ", "")
    if not clean.isdigit():
        raise ValueError(
            "ISBN must contain only digits (after removing hyphens/spaces)"
        )
    if len(clean) != 13:
        raise ValueError("ISBN-13 must be exactly 13 digits")
    total = sum(int(d) * (1 if i % 2 == 0 else 3) for i, d in enumerate(clean))
    return total % 10 == 0
