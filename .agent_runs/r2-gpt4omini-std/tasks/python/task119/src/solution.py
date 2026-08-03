# src/solution.py

def tokenize(expr):
    tokens = []
    current_number = ''
    operators = set('+-*/()^%')
    
    for char in expr:
        if char.isspace():
            continue
        elif char.isdigit() or (char == '.' and current_number):
            current_number += char
        elif char in operators:
            if current_number:
                tokens.append(float(current_number) if '.' in current_number else int(current_number))
                current_number = ''
            tokens.append(char)
        else:
            raise ValueError(f"Invalid character: {char}")
    
    if current_number:
        tokens.append(float(current_number) if '.' in current_number else int(current_number))
    
    return tokens
