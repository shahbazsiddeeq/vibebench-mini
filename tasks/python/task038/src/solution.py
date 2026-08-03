from __future__ import annotations


def caesar(text: str, shift: int) -> str:
    result = []
    shift = shift % 26
    for ch in text:
        if ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            result.append(chr((ord(ch) - base + shift) % 26 + base))
        else:
            result.append(ch)
    return "".join(result)
