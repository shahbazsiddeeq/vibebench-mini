def tokenize(expr):
    tokens = []
    i = 0
    n = len(expr)

    while i < n:
        char = expr[i]

        if char.isspace():
            i += 1
            continue

        if char.isdigit() or (char == '.' and i + 1 < n and expr[i+1].isdigit()):
            j = i
            is_float = False
            while j < n and (expr[j].isdigit() or expr[j] == '.'):
                if expr[j] == '.':
                    if is_float:  # Multiple decimal points
                        raise ValueError(f"Invalid number format at position {j}")
                    is_float = True
                j += 1
            
            num_str = expr[i:j]
            if num_str.startswith('.') and len(num_str) == 1: # Just a dot
                raise ValueError(f"Invalid character: {char} at position {i}")
            if num_str.endswith('.') and len(num_str) > 1: # Number ending with a dot, e.g., "2."
                raise ValueError(f"Invalid number format at position {j-1}")
            if num_str.count('.') > 1:
                raise ValueError(f"Invalid number format at position {i}")

            if is_float:
                tokens.append(float(num_str))
            else:
                tokens.append(int(num_str))
            i = j
            continue

        if char in "+-*/()^%":
            tokens.append(char)
            i += 1
            continue

        raise ValueError(f"Invalid character: {char} at position {i}")

    return tokens
