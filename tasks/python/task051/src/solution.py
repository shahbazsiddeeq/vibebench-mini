from __future__ import annotations


def normalize_case(text: str) -> str:
    chars = list(text.lower())
    capitalize_next = True
    for i, ch in enumerate(chars):
        if ch.isalpha():
            if capitalize_next:
                chars[i] = ch.upper()
                capitalize_next = False
        elif ch in ".!?":
            capitalize_next = True
    return "".join(chars)
