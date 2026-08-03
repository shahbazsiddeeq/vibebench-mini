def render_template(template: str, values: dict) -> str:
    result = []
    i = 0
    n = len(template)
    
    while i < n:
        char = template[i]
        
        if char == '{':
            # Check if it's an escaped brace {{
            if i + 1 < n and template[i + 1] == '{':
                result.append('{')
                i += 2
                continue
            
            # Otherwise, it should be a placeholder {name}
            # Find the closing }
            j = i + 1
            while j < n and template[j] != '}':
                j += 1
            
            if j >= n:
                # No closing brace found
                raise ValueError(f"Unterminated placeholder starting at position {i}")
            
            # Extract the name
            name = template[i + 1:j]
            
            # Validate the name
            if not name:
                raise ValueError("Empty placeholder")
            
            # Check if name contains only valid characters [A-Za-z0-9_]
            for c in name:
                if not (c.isalnum() or c == '_'):
                    raise ValueError(f"Invalid character in placeholder name: {name}")
            
            # Look up the value
            if name not in values:
                raise KeyError(name)
            
            result.append(str(values[name]))
            i = j + 1
            
        elif char == '}':
            # Check if it's an escaped brace }}
            if i + 1 < n and template[i + 1] == '}':
                result.append('}')
                i += 2
                continue
            else:
                # Lone } is an error
                raise ValueError(f"Unmatched closing brace at position {i}")
        
        else:
            # Regular character
            result.append(char)
            i += 1
    
    return ''.join(result)
