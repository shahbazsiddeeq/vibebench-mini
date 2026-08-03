def tokenize(expr):
    import re

    # Define the regex pattern for matching tokens
    token_pattern = re.compile(r'\s*(?:(\d+\.\d+)|(\d+)|([+\-*/^%()]))\s*')

    tokens = []
    pos = 0
    while pos < len(expr):
        match = token_pattern.match(expr, pos)
        if not match:
            raise ValueError(f"Invalid character at position {pos}")

        # Extract the matched groups
        float_num, int_num, operator = match.groups()

        if float_num:
            tokens.append(float(float_num))
        elif int_num:
            tokens.append(int(int_num))
        elif operator:
            tokens.append(operator)

        # Move the position forward
        pos = match.end()

    return tokens
