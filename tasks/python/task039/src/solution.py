from __future__ import annotations

import re

TOKEN = re.compile(r"([0-9]+)([^0-9])", re.DOTALL)


def rle_encode(s: str) -> str:
    if not s:
        return ""
    if any(c in "0123456789" for c in s):
        raise ValueError("input must not contain digits")
    result = []
    count = 1
    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            count += 1
        else:
            result.append(f"{count}{s[i - 1]}")
            count = 1
    result.append(f"{count}{s[-1]}")
    return "".join(result)


def rle_decode(s: str) -> str:
    if not s:
        return ""
    tokens = TOKEN.findall(s)
    if "".join(n + c for n, c in tokens) != s:
        raise ValueError("malformed RLE string")
    parts = []
    for n, c in tokens:
        count = int(n)
        if count == 0:
            raise ValueError("malformed RLE string: zero count")
        parts.append(c * count)
    return "".join(parts)
