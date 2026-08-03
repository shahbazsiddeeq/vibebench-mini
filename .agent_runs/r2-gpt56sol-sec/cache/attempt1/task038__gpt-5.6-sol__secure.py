"""Caesar cipher implementation."""


def caesar(text: str, shift: int) -> str:
    """Shift ASCII letters by ``shift`` positions, preserving case."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if not isinstance(shift, int) or isinstance(shift, bool):
        raise TypeError("shift must be an integer")

    normalized_shift = shift % 26
    result: list[str] = []

    for character in text:
        code = ord(character)

        if ord("A") <= code <= ord("Z"):
            result.append(chr(ord("A") + (code - ord("A") + normalized_shift) % 26))
        elif ord("a") <= code <= ord("z"):
            result.append(chr(ord("a") + (code - ord("a") + normalized_shift) % 26))
        else:
            result.append(character)

    return "".join(result)
