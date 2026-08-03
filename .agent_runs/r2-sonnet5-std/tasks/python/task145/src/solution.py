import re

_NAME_RE = re.compile(r'[A-Za-z0-9_]')


def render_template(template: str, values: dict) -> str:
    """
    Render a template string, substituting placeholders of the form
    {name} with str(values[name]). '{{' becomes '{' and '}}' becomes '}'.

    Raises:
        KeyError: if a placeholder's name is not found in values.
        ValueError: if a brace is malformed (unterminated placeholder,
                    empty placeholder, illegal character in name, or
                    a stray unmatched '}' ).
    """
    result = []
    i = 0
    n = len(template)

    while i < n:
        ch = template[i]

        if ch == '{':
            # Check for escaped '{{'
            if i + 1 < n and template[i + 1] == '{':
                result.append('{')
                i += 2
                continue

            # Attempt to parse a placeholder name
            j = i + 1
            while j < n and _NAME_RE.match(template[j]):
                j += 1

            if j < n and template[j] == '}':
                name = template[i + 1:j]
                if name == '':
                    raise ValueError(
                        f"Empty placeholder at position {i} in template"
                    )
                if name not in values:
                    raise KeyError(name)
                result.append(str(values[name]))
                i = j + 1
                continue
            else:
                # Either hit an illegal character before '}' or ran out
                # of string (unterminated placeholder)
                raise ValueError(
                    f"Malformed placeholder starting at position {i} in template"
                )

        elif ch == '}':
            if i + 1 < n and template[i + 1] == '}':
                result.append('}')
                i += 2
                continue
            else:
                raise ValueError(
                    f"Unmatched '}}' at position {i} in template"
                )

        else:
            result.append(ch)
            i += 1

    return ''.join(result)
