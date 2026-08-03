def tokenize(expr):
    """
    Tokenize an arithmetic expression string into a list of tokens.
    
    Args:
        expr: String containing an arithmetic expression
        
    Returns:
        List of tokens (int, float, or str for operators/parentheses)
        
    Raises:
        ValueError: If the expression contains invalid characters
    """
    if not isinstance(expr, str):
        raise ValueError("Expression must be a string")
    
    tokens = []
    i = 0
    valid_operators = {'+', '-', '*', '/', '(', ')', '^', '%'}
    
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
        
        # Check for numbers (including negative numbers handled as separate tokens)
        if char.isdigit() or char == '.':
            # Extract the full number
            num_str = ''
            has_dot = False
            
            while i < len(expr) and (expr[i].isdigit() or expr[i] == '.'):
                if expr[i] == '.':
                    if has_dot:
                        # Multiple dots in a number is invalid
                        raise ValueError(f"Invalid character in expression: multiple dots in number")
                    has_dot = True
                num_str += expr[i]
                i += 1
            
            # Validate and convert the number
            if num_str == '.':
                raise ValueError(f"Invalid character in expression: standalone dot")
            
            try:
                if has_dot:
                    tokens.append(float(num_str))
                else:
                    tokens.append(int(num_str))
            except ValueError:
                raise ValueError(f"Invalid number format: {num_str}")
            
            continue
        
        # Invalid character
        raise ValueError(f"Invalid character in expression: {char}")
    
    return tokens
