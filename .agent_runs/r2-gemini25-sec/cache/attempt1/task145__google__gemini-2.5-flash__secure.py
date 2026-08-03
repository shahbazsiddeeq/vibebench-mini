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
        if template[i] == '{':
            if i + 1 < n and template[i+1] == '{':
                result.append('{')
                i += 2
            else:
                # Potential placeholder or invalid '{'
                start_brace_idx = i
                i += 1
                name_start_idx = i
                while i < n and template[i].isalnum() or template[i] == '_':
                    i += 1
                
                name = template[name_start_idx:i]

                if not name: # Empty placeholder like {} or { }
                    raise ValueError(f"Invalid placeholder: empty or malformed name at index {start_brace_idx}")

                if i < n and template[i] == '}':
                    # Valid placeholder {name}
                    if not re.fullmatch(r'[A-Za-z0-9_]+', name):
                        raise ValueError(f"Invalid characters in placeholder name '{name}' at index {start_brace_idx}")
                    
                    if name not in values:
                        raise KeyError(name)
                    result.append(str(values[name]))
                    i += 1 # Move past '}'
                else:
                    # Unterminated placeholder or invalid character after '{'
                    # e.g., {name, {name!, {name
                    raise ValueError(f"Invalid placeholder or unterminated '{' at index {start_brace_idx}")
        elif template[i] == '}':
            if i + 1 < n and template[i+1] == '}':
                result.append('}')
                i += 2
            else:
                # Lone '}'
                raise ValueError(f"Unmatched '}}' at index {i}")
        else:
            result.append(template[i])
            i += 1

    return "".join(result)
