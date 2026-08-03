def tokenize(expr):
    """
    Tokenize an arithmetic expression string into a list of tokens.
    
    Numbers with '.' become float, numbers without become int.
    Single-character operators and parentheses: + - * / ( ) ^ %
    Whitespace is ignored.
    Raises ValueError for any other character.
    """
    tokens = []
    i = 0
    
    while i < len(expr):
        # Skip whitespace
        if expr[i].isspace():
            i += 1
            continue
        
        # Check for operators and parentheses
        if expr[i] in "+-*/%()^":
            tokens.append(expr[i])
            i += 1
            continue
        
        # Check for numbers
        if expr[i].isdigit() or (expr[i] == '.' and i + 1 < len(expr) and expr[i + 1].isdigit()):
            j = i
            has_dot = False
            
            while j < len(expr) and (expr[j].isdigit() or expr[j] == '.'):
                if expr[j] == '.':
                    if has_dot:
                        # Multiple dots in a number
                        break
                    has_dot = True
                j += 1
            
            num_str = expr[i:j]
            
            if has_dot:
                tokens.append(float(num_str))
            else:
                tokens.append(int(num_str))
            
            i = j
            continue
        
        # Invalid character
        raise ValueError(f"Invalid character: {expr[i]}")
    
    return tokens
