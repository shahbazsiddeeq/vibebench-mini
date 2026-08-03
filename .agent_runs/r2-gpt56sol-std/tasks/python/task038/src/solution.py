def caesar(text: str, shift: int) -> str:
    """Shift ASCII letters by the given amount, preserving case."""
    shift %= 26
    result = []

    for char in text:
        if "A" <= char <= "Z":
            result.append(chr((ord(char) - ord("A") + shift) % 26 + ord("A")))
        elif "a" <= char <= "z":
            result.append(chr((ord(char) - ord("a") + shift) % 26 + ord("a")))
        else:
            result.append(char)

    return "".join(result)
