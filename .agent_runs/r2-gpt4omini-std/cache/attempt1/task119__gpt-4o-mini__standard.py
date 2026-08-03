# src/solution.py

import re

def tokenize(expr):
    # Define a regex pattern to match numbers, operators, and parentheses
    token_pattern = r'\s*(?:(\d+\.\d+)|(\d+)|([+\-*/^%()]))\s*'
    tokens = []
    
    for match in re.finditer(token_pattern, expr):
        float_token = match.group(1)
        int_token = match.group(2)
        operator_token = match.group(3)
        
        if float_token is not None:
            tokens.append(float(float_token))
        elif int_token is not None:
            tokens.append(int(int_token))
        elif operator_token is not None:
            tokens.append(operator_token)
        else:
            raise ValueError(f"Invalid character in expression: {expr}")
    
    return tokens
