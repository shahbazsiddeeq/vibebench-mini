def tokenize(expr):
    """
    Tokenize an arithmetic expression string into a list of tokens.
    
    Numbers with '.' become float, without become int.
    Operators + - * / ( ) ^ % become str.
    Whitespace is ignored.
    Raises ValueError for invalid characters.
    """
    tokens = []
    i = 0
    operators = {'+', '-', '*', '/', '(', ')', '^', '%'}
    
    while i < len(expr):
        char = expr[i]
        
        # Skip whitespace
        if char.isspace():
            i += 1
            continue
        
        # Check for operators
        if char in operators:
            tokens.append(char)
            i += 1
            continue
        
        # Check for numbers (digits or decimal point)
        if char.isdigit() or char == '.':
            # Collect the full number
            num_str = ''
            has_dot = False
            
            while i < len(expr) and (expr[i].isdigit() or expr[i] == '.'):
                if expr[i] == '.':
                    has_dot = True
                num_str += expr[i]
                i += 1
            
            # Convert to appropriate type
            if has_dot:
                tokens.append(float(num_str))
            else:
                tokens.append(int(num_str))
            continue
        
        # Invalid character
        raise ValueError(f"Invalid character: {char}")
    
    return tokens
