"""Run-length encoding and decoding utilities."""


def rle_encode(s: str) -> str:
    """Encode consecutive character runs as count followed by character."""
    if not isinstance(s, str):
        raise TypeError("s must be a string")
    if any("0" <= char <= "9" for char in s):
        raise ValueError("input must not contain ASCII digits")
    if not s:
        return ""

    encoded: list[str] = []
    run_char = s[0]
    run_count = 1

    for char in s[1:]:
        if char == run_char:
            run_count += 1
        else:
            encoded.append(f"{run_count}{run_char}")
            run_char = char
            run_count = 1

    encoded.append(f"{run_count}{run_char}")
    return "".join(encoded)


def rle_decode(s: str) -> str:
    """Decode count-character run-length encoding."""
    if not isinstance(s, str):
        raise TypeError("s must be a string")

    decoded: list[str] = []
    index = 0
    length = len(s)

    while index < length:
        count_start = index
        while index < length and "0" <= s[index] <= "9":
            index += 1

        if count_start == index or index == length:
            raise ValueError("malformed run-length encoding")

        count_text = s[count_start:index]
        count = int(count_text)
        if count == 0:
            raise ValueError("run count must be non-zero")

        decoded.append(s[index] * count)
        index += 1

    return "".join(decoded)
