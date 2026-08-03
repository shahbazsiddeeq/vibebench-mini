import re

def render_template(template: str, values: dict) -> str:
    def replace_placeholder(match):
        text = match.group(0)
        if text == '{{':
            return '{'
        elif text == '}}':
            return '}'
        elif text.startswith('{') and text.endswith('}'):
            name = text[1:-1]
            if not re.match(r'^[A-Za-z0-9_]+$', name):
                raise ValueError(f"Invalid placeholder name: {name}")
            if name not in values:
                raise KeyError(name)
            return str(values[name])
        else:
            raise ValueError(f"Invalid placeholder: {text}")

    pattern = re.compile(r'{{|}}|{[A-Za-z0-9_]*}|{[^}]*}|}')
    return pattern.sub(replace_placeholder, template)
