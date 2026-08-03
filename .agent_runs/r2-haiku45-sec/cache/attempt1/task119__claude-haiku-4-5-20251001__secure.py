"""Simple Expression Tokenizer module."""

import re


def tokenize(expr: str) -> list:
    """
    Tokenize an arithmetic expression string into a list of tokens.
    
    Numbers containing '.' become floats, numbers without become ints.
    Single-character operators and parentheses (+ - * / ( ) ^ %) are emitted as strings.
    Whitespace is ignored.
    
    Args:
        expr: An arithmetic expression string to tokenize.
        
    Returns:
        A list of tokens (int, float, or str).
        
    Raises:
        ValueError: If an invalid character is encountered.
    """
    if not isinstance(expr, str):
        raise ValueError("Expression must be a string")
    
    # Valid single-character tokens
    valid_operators = {'+', '-', '*', '/', '(', ')', '^', '%'}
    
    tokens = []
    i = 0
    
    while i < len(expr):
        char = expr[i]
        
        # Skip whitespace
        if char.isspace():
            i += 1
            continue
        
        # Check for operators and parentheses
        if char in valid_operators:
            tokens.append(char)
            i += 1
            continue
        
        # Check for numbers (including decimals)
        if char.isdigit() or (char == '.' and i + 1 < len(expr) and expr[i + 1].isdigit()):
            # Extract the full number
            num_start = i
            has_dot = False
            
            while i < len(expr) and (expr[i].isdigit() or expr[i] == '.'):
                if expr[i] == '.':
                    if has_dot:
                        # Multiple dots in a number is invalid
                        raise ValueError(f"Invalid number format at position {num_start}")
                    has_dot = True
                i += 1
            
            num_str = expr[num_start:i]
            
            # Convert to appropriate type
            if has_dot:
                tokens.append(float(num_str))
            else:
                tokens.append(int(num_str))
            continue
        
        # Invalid character
        raise ValueError(f"Invalid character '{char}' at position {i}")
    
    return tokens
