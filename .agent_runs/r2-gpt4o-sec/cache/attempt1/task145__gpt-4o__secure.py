import re

def render_template(template: str, values: dict) -> str:
    # Regular expression to match placeholders and escaped braces
    pattern = re.compile(r'({{)|(}})|{([A-Za-z0-9_]+)}|({)|(})')

    def replace(match):
        if match.group(1):  # '{{'
            return '{'
        elif match.group(2):  # '}}'
            return '}'
        elif match.group(3):  # '{name}'
            name = match.group(3)
            if name in values:
                return str(values[name])
            else:
                raise KeyError(name)
        elif match.group(4):  # '{' not followed by a valid name
            raise ValueError("Invalid placeholder start")
        elif match.group(5):  # '}' not preceded by a valid placeholder
            raise ValueError("Unmatched closing brace")
        return match.group(0)

    # Substitute placeholders and handle errors
    result = pattern.sub(replace, template)
    return result
