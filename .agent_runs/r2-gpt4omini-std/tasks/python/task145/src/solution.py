import re

def render_template(template: str, values: dict) -> str:
    result = []
    i = 0
    length = len(template)

    while i < length:
        if template[i] == '{':
            if i + 1 < length and template[i + 1] == '{':
                result.append('{')
                i += 2
            else:
                # Start of a placeholder
                j = i + 1
                while j < length and re.match(r'[A-Za-z0-9_]', template[j]):
                    j += 1
                if j == i + 1 or (j < length and template[j] != '}'):
                    raise ValueError("Invalid placeholder")
                placeholder_name = template[i + 1:j]
                if placeholder_name not in values:
                    raise KeyError(placeholder_name)
                result.append(str(values[placeholder_name]))
                i = j + 1
        elif template[i] == '}':
            if i + 1 < length and template[i + 1] == '}':
                result.append('}')
                i += 2
            else:
                raise ValueError("Unmatched '}'")
        else:
            result.append(template[i])
            i += 1

    return ''.join(result)
