import re


def to_snake(s: str) -> str:
    """Convert a camelCase or PascalCase string to lowercase snake_case."""
    s = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", s)
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s)
    return s.lower()


def to_camel(s: str) -> str:
    """Convert a snake_case string to lower camelCase."""
    parts = s.split("_")
    result = parts[0] + "".join(
        part[:1].upper() + part[1:] for part in parts[1:] if part
    )
    return result[:1].lower() + result[1:]
