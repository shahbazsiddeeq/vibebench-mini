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
        template: The template string containing placeholders.
        values: A dictionary mapping placeholder names to their substitution values.

    Returns:
        The rendered string with placeholders substituted.

    Raises:
        KeyError: If a valid placeholder's name is not a key in values.
        ValueError: If a '{' is not part of '{{' nor a valid '{name}'
                    (this includes empty '{}', a name with an illegal character,
                    or an unterminated '{name'), or if a '}' is not part of '}}'
                    and does not close a placeholder.
    """
    if not isinstance(template, str):
        raise TypeError("template must be a string")
    if not isinstance(values, dict):
        raise TypeError("values must be a dictionary")

    result = []
    i = 0
    n = len(template)

    while i < n:
        if template[i:i+2] == '{{':
            result.append('{')
            i += 2
        elif template[i:i+2] == '}}':
            result.append('}')
            i += 2
        elif template[i] == '{':
            start_brace_idx = i
            i += 1
            # Find the closing brace
            end_brace_idx = -1
            for j in range(i, n):
                if template[j] == '}':
                    end_brace_idx = j
                    break

            if end_brace_idx == -1:
                raise ValueError(f"Unterminated placeholder starting at index {start_brace_idx}")

            name = template[i:end_brace_idx]
            if not re.fullmatch(r'[A-Za-z0-9_]+', name):
                raise ValueError(f"Invalid placeholder name '{name}' at index {start_brace_idx}")

            if name not in values:
                raise KeyError(name)

            result.append(str(values[name]))
            i = end_brace_idx + 1
        elif template[i] == '}':
            raise ValueError(f"Unexpected '}}' at index {i}")
        else:
            result.append(template[i])
            i += 1

    return "".join(result)
