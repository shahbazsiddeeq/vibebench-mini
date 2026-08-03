import re

def render_template(template: str, values: dict) -> str:
    if not isinstance(template, str):
        raise ValueError("Template must be a string.")
    if not isinstance(values, dict):
        raise ValueError("Values must be a dictionary.")

    result = []
    pos = 0
    pattern = re.compile(r'(\{\{|\}\}|{([A-Za-z0-9_]+)})')

    for match in pattern.finditer(template):
        # Append text before the match
        result.append(template[pos:match.start()])
        pos = match.end()

        if match.group(0) == '{{':
            result.append('{')
        elif match.group(0) == '}}':
            result.append('}')
        else:
            name = match.group(2)
            if name is None:
                raise ValueError("Invalid placeholder format.")
            if name not in values:
                raise KeyError(name)
            result.append(str(values[name]))

    # Append any remaining text after the last match
    result.append(template[pos:])

    # Join the result list into a single string
    final_result = ''.join(result)

    # Check for unmatched braces
    if final_result.count('{') != final_result.count('}'):
        raise ValueError("Unmatched braces in template.")

    return final_result
