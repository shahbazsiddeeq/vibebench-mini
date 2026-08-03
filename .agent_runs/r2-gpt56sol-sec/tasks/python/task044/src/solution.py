"""Utilities for converting between camelCase and snake_case."""


def _require_string(value: object, function_name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{function_name}() argument must be a string")
    return value


def to_snake(s: str) -> str:
    """Convert a camelCase or PascalCase string to lowercase snake_case."""
    value = _require_string(s, "to_snake")
    result: list[str] = []

    for index, char in enumerate(value):
        if index > 0 and char.isupper():
            previous = value[index - 1]
            next_char = value[index + 1] if index + 1 < len(value) else ""

            starts_word = previous.islower() or previous.isdigit()
            ends_acronym = previous.isupper() and next_char.islower()

            if (starts_word or ends_acronym) and result[-1] != "_":
                result.append("_")

        result.append(char.lower())

    return "".join(result)


def to_camel(s: str) -> str:
    """Convert an underscore-separated string to lower camelCase."""
    value = _require_string(s, "to_camel")
    parts = value.split("_")

    combined = parts[0] + "".join(
        part[:1].upper() + part[1:] for part in parts[1:] if part
    )

    if not combined:
        return ""

    return combined[:1].lower() + combined[1:]
