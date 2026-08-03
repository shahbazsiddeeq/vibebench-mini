def render_template(template: str, values: dict) -> str:
    """
    Render a template by substituting placeholders with values.
    
    Args:
        template: Template string with {name} placeholders
        values: Dictionary mapping placeholder names to values
        
    Returns:
        Rendered string with substitutions applied
        
    Raises:
        KeyError: If a placeholder name is not in values
        ValueError: If template syntax is invalid
    """
    if not isinstance(template, str):
        raise TypeError("template must be a string")
    if not isinstance(values, dict):
        raise TypeError("values must be a dictionary")
    
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
            
            # It's a placeholder - find the closing }
            j = i + 1
            
            # Find the end of the placeholder name
            while j < n and template[j] != '}':
                j += 1
            
            # Check if we found a closing brace
            if j >= n:
                raise ValueError(f"Unterminated placeholder starting at position {i}")
            
            # Extract the name
            name = template[i + 1:j]
            
            # Validate the name is not empty
            if not name:
                raise ValueError("Empty placeholder {} is not allowed")
            
            # Validate the name contains only allowed characters
            for idx, c in enumerate(name):
                if not (c.isalnum() or c == '_'):
                    raise ValueError(f"Invalid character in placeholder name: '{c}'")
            
            # Look up the value
            if name not in values:
                raise KeyError(name)
            
            # Substitute the value
            result.append(str(values[name]))
            i = j + 1
            
        elif char == '}':
            # Check if it's an escaped brace }}
            if i + 1 < n and template[i + 1] == '}':
                result.append('}')
                i += 2
                continue
            
            # Lone } is an error
            raise ValueError(f"Unmatched closing brace at position {i}")
        
        else:
            # Regular character - copy verbatim
            result.append(char)
            i += 1
    
    return ''.join(result)
