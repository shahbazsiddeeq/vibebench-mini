# src/solution.py

import re

def tokenize(expr):
    # Define the regular expression pattern for tokenizing
    token_pattern = r"""
        (?P<NUMBER>\d+(\.\d+)?) |  # Matches integers and floats
        (?P<OPERATOR>[+\-*/^%()]) |  # Matches operators and parentheses
        (?P<WHITESPACE>\s+) |  # Matches whitespace
        (?P<INVALID>.)  # Matches any invalid character
    """
    
    # Compile the regular expression with verbose flag for readability
    token_regex = re.compile(token_pattern, re.VERBOSE)
    
    tokens = []
    
    for match in token_regex.finditer(expr):
        kind = match.lastgroup
        value = match.group(kind)
        
        if kind == 'NUMBER':
            # Convert to int or float
            if '.' in value:
                tokens.append(float(value))
            else:
                tokens.append(int(value))
        elif kind == 'OPERATOR':
            tokens.append(value)
        elif kind == 'WHITESPACE':
            continue  # Ignore whitespace
        elif kind == 'INVALID':
            raise ValueError(f"Invalid character found: {value}")
    
    return tokens
