"""Template placeholder substitution."""

import re


_PLACEHOLDER_NAME = re.compile(r"[A-Za-z0-9_]+\Z")


def render_template(template: str, values: dict) -> str:
    """Render placeholders and escaped braces in *template*."""
    result = []
    index = 0
    length = len(template)

    while index < length:
        char = template[index]

        if char == "{":
            if index + 1 < length and template[index + 1] == "{":
                result.append("{")
                index += 2
                continue

            closing = template.find("}", index + 1)
            if closing == -1:
                raise ValueError("Unterminated placeholder")

            name = template[index + 1 : closing]
            if _PLACEHOLDER_NAME.fullmatch(name) is None:
                raise ValueError(f"Invalid placeholder: {name!r}")

            if name not in values:
                raise KeyError(name)

            result.append(str(values[name]))
            index = closing + 1
            continue

        if char == "}":
            if index + 1 < length and template[index + 1] == "}":
                result.append("}")
                index += 2
                continue
            raise ValueError("Unmatched closing brace")

        result.append(char)
        index += 1

    return "".join(result)
