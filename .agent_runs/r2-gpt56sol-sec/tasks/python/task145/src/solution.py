"""Secure, deterministic template placeholder substitution."""


def render_template(template: str, values: dict) -> str:
    """Render placeholders and escaped braces in *template*.

    Placeholders have the form ``{name}``, where *name* contains only ASCII
    letters, digits, or underscores. Double braces represent literal braces.
    """
    if not isinstance(template, str):
        raise TypeError("template must be a string")
    if not isinstance(values, dict):
        raise TypeError("values must be a dictionary")

    output: list[str] = []
    index = 0
    length = len(template)

    while index < length:
        char = template[index]

        if char == "{":
            if index + 1 < length and template[index + 1] == "{":
                output.append("{")
                index += 2
                continue

            name_start = index + 1
            name_end = name_start

            while name_end < length:
                current = template[name_end]
                if (
                    "A" <= current <= "Z"
                    or "a" <= current <= "z"
                    or "0" <= current <= "9"
                    or current == "_"
                ):
                    name_end += 1
                else:
                    break

            if name_end == name_start:
                raise ValueError("invalid placeholder")
            if name_end >= length or template[name_end] != "}":
                raise ValueError("invalid placeholder")

            name = template[name_start:name_end]
            if name not in values:
                raise KeyError(name)

            output.append(str(values[name]))
            index = name_end + 1
            continue

        if char == "}":
            if index + 1 < length and template[index + 1] == "}":
                output.append("}")
                index += 2
                continue
            raise ValueError("unmatched closing brace")

        output.append(char)
        index += 1

    return "".join(output)
