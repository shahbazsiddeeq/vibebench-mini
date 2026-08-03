def tokenize(expr: str) -> list:
    tokens = []
    i = 0
    valid_ops = set("+-*/()^%")
    while i < len(expr):
        ch = expr[i]
        if ch.isspace():
            i += 1
            continue
        if ch.isdigit() or (ch == "." and i + 1 < len(expr) and expr[i + 1].isdigit()):
            j = i
            while j < len(expr) and (expr[j].isdigit() or expr[j] == "."):
                j += 1
            num_str = expr[i:j]
            tokens.append(float(num_str) if "." in num_str else int(num_str))
            i = j
        elif ch in valid_ops:
            tokens.append(ch)
            i += 1
        else:
            raise ValueError(f"Invalid character: {ch!r}")
    return tokens
