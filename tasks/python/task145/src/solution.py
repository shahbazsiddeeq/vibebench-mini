def render_template(template: str, values: dict) -> str:
    """Substitute {name} placeholders in template; {{ and }} are literal braces."""
    out = []
    i = 0
    n = len(template)
    while i < n:
        c = template[i]
        if c == "{":
            if i + 1 < n and template[i + 1] == "{":
                out.append("{")
                i += 2
                continue
            j = i + 1
            while j < n and template[j].isascii() and (
                template[j].isalnum() or template[j] == "_"
            ):
                j += 1
            if j == i + 1 or j >= n or template[j] != "}":
                raise ValueError(f"invalid placeholder at index {i}")
            name = template[i + 1 : j]
            if name not in values:
                raise KeyError(name)
            out.append(str(values[name]))
            i = j + 1
        elif c == "}":
            if i + 1 < n and template[i + 1] == "}":
                out.append("}")
                i += 2
                continue
            raise ValueError(f"unmatched '}}' at index {i}")
        else:
            out.append(c)
            i += 1
    return "".join(out)
