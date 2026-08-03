import re

def render_template(template: str, values: dict) -> str:
    """
    Substitutes placeholders in template with values from the values dict.
    
    Placeholders are {name} where name matches [A-Za-z0-9_]+
    {{ produces a single {
    }} produces a single }
    
    Raises KeyError if a placeholder name is not in values.
    Raises ValueError if braces are malformed.
    """
    result = []
    i = 0
    
    while i < len(template):
        char = template[i]
        
        if char == '{':
            # Check for {{
            if i + 1 < len(template) and template[i + 1] == '{':
                result.append('{')
                i += 2
            else:
                # This should be a placeholder {name}
                # Find the closing }
                j = i + 1
                name = ""
                
                # Collect characters that are valid in a name
                while j < len(template):
                    c = template[j]
                    if c == '}':
                        break
                    if re.match(r'[A-Za-z0-9_]', c):
                        name += c
                        j += 1
                    else:
                        # Invalid character in placeholder name
                        raise ValueError(f"Invalid character in placeholder name")
                
                # Check if we found a closing }
                if j >= len(template):
                    raise ValueError(f"Unterminated placeholder")
                
                # Check if name is empty
                if not name:
                    raise ValueError(f"Empty placeholder name")
                
                # Look up the value
                if name not in values:
                    raise KeyError(name)
                
                result.append(str(values[name]))
                i = j + 1
        
        elif char == '}':
            # Check for }}
            if i + 1 < len(template) and template[i + 1] == '}':
                result.append('}')
                i += 2
            else:
                # Lone closing brace
                raise ValueError(f"Unmatched closing brace")
        
        else:
            # Regular character
            result.append(char)
            i += 1
    
    return ''.join(result)
