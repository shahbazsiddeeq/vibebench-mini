# src/solution.py

import re

def tokenize(expr: str):
    # Validate input: ensure it's a string
    if not isinstance(expr, str):
        raise ValueError("Input must be a string.")
    
    # Define a regex pattern for valid tokens
    token_pattern = r'\s*([0-9]*\.[0-9]+|[0-9]+|[+\-*/()^%])\s*'
    
    tokens = []
    for match in re.finditer(token_pattern, expr):
        token = match.group(1)
        if re.match(r'^[0-9]*\.[0-9]+$', token):  # Float
            tokens.append(float(token))
        elif re.match(r'^[0-9]+$', token):  # Integer
            tokens.append(int(token))
        elif token in "+-*/()^%":  # Operators and parentheses
            tokens.append(token)
        else:
            raise ValueError(f"Invalid character found: {token}")
    
    return tokens
