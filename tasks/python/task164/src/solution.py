"""Vigenere polyalphabetic cipher (standard library only)."""


def _key_shifts(key):
    if not isinstance(key, str):
        raise TypeError("key must be a str")
    if len(key) == 0:
        raise ValueError("key must be non-empty")
    shifts = []
    for c in key:
        if not (("a" <= c <= "z") or ("A" <= c <= "Z")):
            raise ValueError("key must contain only ASCII letters")
        shifts.append(ord(c.lower()) - 97)
    return shifts


def _transform(text, key, sign):
    if not isinstance(text, str):
        raise TypeError("text must be a str")
    shifts = _key_shifts(key)
    n = len(shifts)
    out = []
    ki = 0
    for ch in text:
        if "A" <= ch <= "Z":
            base = 65
        elif "a" <= ch <= "z":
            base = 97
        else:
            out.append(ch)
            continue
        shift = sign * shifts[ki % n]
        out.append(chr((ord(ch) - base + shift) % 26 + base))
        ki += 1
    return "".join(out)


def vigenere_encrypt(plaintext: str, key: str) -> str:
    return _transform(plaintext, key, 1)


def vigenere_decrypt(ciphertext: str, key: str) -> str:
    return _transform(ciphertext, key, -1)
