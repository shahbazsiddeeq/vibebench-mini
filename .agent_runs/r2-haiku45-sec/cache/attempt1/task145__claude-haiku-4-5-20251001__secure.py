import re


def render_template(template: str, values: dict) -> str:
    """
    Substitutes placeholders in template with values from the values dict.
    
    Placeholders are '{name}' where name matches [A-Za-z0-9_]+.
    '{{' produces '{' and '}}' produces '}'.
    
    Raises:
        KeyError: if a placeholder name is not in values
        ValueError: if template has invalid syntax (unmatched braces, empty placeholder, etc.)
    """
    if not template:
        return ""
    
    result = []
    i = 0
    
    while i < len(template):
        char = template[i]
        
        if char == '{':
            # Check for escaped brace {{
            if i + 1 < len(template) and template[i + 1] == '{':
                result.append('{')
                i += 2
                continue
            
            # Check for placeholder {name}
            # Find the closing brace
            j = i + 1
            name_chars = []
            
            # Collect valid name characters
            while j < len(template):
                c = template[j]
                if c == '}':
                    # Found closing brace
                    break
                # Check if character is valid for name: [A-Za-z0-9_]
                if not (c.isalnum() or c == '_'):
                    # Invalid character in placeholder name
                    raise ValueError(f"Invalid character in placeholder name: {c}")
                name_chars.append(c)
                j += 1
            
            # Check if we found a closing brace
            if j >= len(template):
                # Unterminated placeholder
                raise ValueError("Unterminated placeholder")
            
            # Check if name is empty
            if not name_chars:
                raise ValueError("Empty placeholder name")
            
            name = ''.join(name_chars)
            
            # Look up the name in values
            if name not in values:
                raise KeyError(name)
            
            # Substitute the value
            result.append(str(values[name]))
            i = j + 1
            continue
        
        elif char == '}':
            # Check for escaped brace }}
            if i + 1 < len(template) and template[i + 1] == '}':
                result.append('}')
                i += 2
                continue
            
            # Unmatched closing brace
            raise ValueError("Unmatched closing brace")
        
        else:
            # Regular character
            result.append(char)
            i += 1
    
    return ''.join(result)
