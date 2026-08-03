import re

_TOKEN_RE = re.compile(r"(\d+)(\D)")


def rle_encode(s: str) -> str:
    if any(ch.isdigit() for ch in s):
        raise ValueError("Input must not contain digits")

    if s == "":
        return ""

    result = []
    prev_char = s[0]
    count = 1
    for ch in s[1:]:
        if ch == prev_char:
            count += 1
        else:
            result.append(f"{count}{prev_char}")
            prev_char = ch
            count = 1
    result.append(f"{count}{prev_char}")
    return "".join(result)


def rle_decode(s: str) -> str:
    if s == "":
        return ""

    pos = 0
    length = len(s)
    result = []

    while pos < length:
        match = _TOKEN_RE.match(s, pos)
        if not match:
            raise ValueError("Malformed input")
        count_str, char = match.groups()
        count = int(count_str)
        if count == 0:
            raise ValueError("Count must be non-zero")
        result.append(char * count)
        pos = match.end()

    if pos != length:
        raise ValueError("Malformed input")

    return "".join(result)
