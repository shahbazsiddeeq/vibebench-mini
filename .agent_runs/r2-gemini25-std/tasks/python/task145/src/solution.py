import re

def render_template(template: str, values: dict) -> str:
    """
    Substitutes placeholders in a template string.

    A placeholder is '{name}' where name is one or more ASCII letters, digits,
    or underscores (regex [A-Za-z0-9_]+); it is replaced by str(values[name]).
    The literal sequence '{{' produces a single '{' and '}}' produces a single '}'.
    Scanning is strictly left-to-right and case-sensitive; every other character
    (including non-ASCII/Unicode) is copied verbatim.

    Args:
        template: The template string.
        values: A dictionary mapping placeholder names to their substitution values.

    Returns:
        The rendered string.

    Raises:
        KeyError: If a valid placeholder's name is not a key in values.
        ValueError: If a '{' is not part of '{{' nor a valid '{name}',
                    or if a '}' is not part of '}}' and does not close a placeholder.
    """
    if not template:
        return ""

    result = []
    i = 0
    n = len(template)

    while i < n:
        if template[i] == '{':
            if i + 1 < n and template[i+1] == '{':
                result.append('{')
                i += 2
            else:
                # Potential placeholder or invalid '{'
                j = i + 1
                while j < n and template[j].isalnum() or template[j] == '_':
                    j += 1

                if j < n and template[j] == '}':
                    name = template[i+1:j]
                    if not name:
                        raise ValueError(f"Empty placeholder '{{}}' at position {i}")
                    if not re.fullmatch(r'[A-Za-z0-9_]+', name):
                        raise ValueError(f"Invalid character in placeholder name '{name}' at position {i}")
                    
                    if name not in values:
                        raise KeyError(name)
                    result.append(str(values[name]))
                    i = j + 1
                else:
                    # Invalid '{' (e.g., '{', '{name', '{name }', '{name!')
                    raise ValueError(f"Invalid placeholder or unescaped '{{' at position {i}")
        elif template[i] == '}':
            if i + 1 < n and template[i+1] == '}':
                result.append('}')
                i += 2
            else:
                # Unmatched '}'
                raise ValueError(f"Unmatched '}}' at position {i}")
        else:
            result.append(template[i])
            i += 1

    return "".join(result)
