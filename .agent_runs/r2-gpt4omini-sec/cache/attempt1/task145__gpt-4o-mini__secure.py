# src/solution.py

import re

def render_template(template: str, values: dict) -> str:
    # Validate input types
    if not isinstance(template, str):
        raise TypeError("Template must be a string.")
    if not isinstance(values, dict):
        raise TypeError("Values must be a dictionary.")

    # Regular expression for matching placeholders
    placeholder_pattern = re.compile(r'\{([A-Za-z0-9_]+)\}|\{\{|\}\}')
    
    result = []
    pos = 0

    for match in placeholder_pattern.finditer(template):
        # Append the text before the match
        result.append(template[pos:match.start()])
        pos = match.end()

        if match.group(0) == '{{':
            result.append('{')
        elif match.group(0) == '}}':
            result.append('}')
        else:
            name = match.group(1)
            if name is None:
                raise ValueError("Invalid placeholder format.")
            if name not in values:
                raise KeyError(name)
            result.append(str(values[name]))

    # Append any remaining text after the last match
    result.append(template[pos:])

    # Join the result list into a single string
    final_result = ''.join(result)

    # Check for any unmatched braces
    if '{' in final_result or '}' in final_result:
        raise ValueError("Unmatched braces in template.")

    return final_result
