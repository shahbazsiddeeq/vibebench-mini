import re


def to_snake(s: str) -> str:
    """Convert camelCase (or PascalCase) to snake_case, keeping acronyms together."""
    s1 = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', s)
    s2 = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s1)
    return s2.lower()


def to_camel(s: str) -> str:
    """Convert snake_case to camelCase."""
    parts = s.split('_')
    if not parts:
        return s
    first = parts[0].lower()
    rest = [p[:1].upper() + p[1:].lower() if p else '' for p in parts[1:]]
    return first + ''.join(rest)
