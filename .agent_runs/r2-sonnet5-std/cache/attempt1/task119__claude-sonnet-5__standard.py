import re

def tokenize(expr):
    tokens = []
    i = 0
    n = len(expr)
    operators = set("+-*/()^%")
    while i < n:
        c = expr[i]
        if c.isspace():
            i += 1
            continue
        if c.isdigit() or c == '.':
            j = i
            has_dot = False
            while j < n and (expr[j].isdigit() or expr[j] == '.'):
                if expr[j] == '.':
                    has_dot = True
                j += 1
            num_str = expr[i:j]
            if has_dot:
                tokens.append(float(num_str))
            else:
                tokens.append(int(num_str))
            i = j
        elif c in operators:
            tokens.append(c)
            i += 1
        else:
            raise ValueError(f"Invalid character: {c}")
    return tokens
