"""Simple arithmetic expression tokenizer."""

_OPERATORS = frozenset("+-*/()^%")


def tokenize(expr: str) -> list[int | float | str]:
    """Split an arithmetic expression into numbers and operator tokens."""
    if not isinstance(expr, str):
        raise TypeError("expr must be a string")

    tokens: list[int | float | str] = []
    index = 0

    while index < len(expr):
        char = expr[index]

        if char.isspace():
            index += 1
            continue

        if char in _OPERATORS:
            tokens.append(char)
            index += 1
            continue

        if char.isascii() and char.isdigit() or (
            char == "."
            and index + 1 < len(expr)
            and expr[index + 1].isascii()
            and expr[index + 1].isdigit()
        ):
            start = index
            dot_count = 0

            while index < len(expr):
                current = expr[index]
                if current.isascii() and current.isdigit():
                    index += 1
                elif current == ".":
                    dot_count += 1
                    if dot_count > 1:
                        raise ValueError(f"invalid number at position {start}")
                    index += 1
                else:
                    break

            text = expr[start:index]
            tokens.append(float(text) if "." in text else int(text))
            continue

        raise ValueError(f"invalid character {char!r} at position {index}")

    return tokens
