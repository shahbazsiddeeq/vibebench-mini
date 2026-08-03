import re

def render_template(template: str, values: dict) -> str:
    """
    Substitutes placeholders in template. A placeholder is '{name}' where name is one or more
    ASCII letters, digits, or underscores (regex [A-Za-z0-9_]+); it is replaced by
    str(values[name]). The literal sequence '{{' produces a single '{' and '}}' produces a
    single '}'. Scanning is strictly left-to-right and case-sensitive; every other character
    (including non-ASCII/Unicode) is copied verbatim.

    Args:
        template: The template string containing placeholders.
        values: A dictionary mapping placeholder names to their substitution values.

    Returns:
        The rendered string with placeholders substituted.

    Raises:
        KeyError: If a valid placeholder's name is not a key in values.
        ValueError: If a '{' is not part of '{{' nor a valid '{name}' (this includes empty '{}',
                    a name with an illegal character, or an unterminated '{name'), or if a '}'
                    is not part of '}}' and does not close a placeholder.
    """
    if not template:
        return ""

    result_parts = []
    i = 0
    n = len(template)

    while i < n:
        if template[i:i+2] == '{{':
            result_parts.append('{')
            i += 2
        elif template[i:i+2] == '}}':
            result_parts.append('}')
            i += 2
        elif template[i] == '{':
            # Potential placeholder
            j = i + 1
            while j < n and template[j].isalnum() or template[j] == '_':
                j += 1

            if j == i + 1: # Empty name or starts with illegal char
                raise ValueError(f"Invalid placeholder or unescaped '{' at position {i}")

            name = template[i+1:j]

            if j < n and template[j] == '}':
                # Valid placeholder found
                if name not in values:
                    raise KeyError(name)
                result_parts.append(str(values[name]))
                i = j + 1
            else:
                # Unterminated placeholder or illegal character after name
                raise ValueError(f"Invalid placeholder or unescaped '{' at position {i}")
        elif template[i] == '}':
            # Unmatched '}'
            raise ValueError(f"Unmatched '}}' at position {i}")
        else:
            result_parts.append(template[i])
            i += 1

    return "".join(result_parts)
