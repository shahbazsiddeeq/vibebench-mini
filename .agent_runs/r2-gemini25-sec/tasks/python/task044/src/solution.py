import re

def to_snake(s: str) -> str:
    if not isinstance(s, str):
        raise TypeError("Input must be a string.")
    if not s:
        return ""

    # Handle acronyms: look for uppercase sequences followed by a lowercase letter
    # or end of string. Insert underscore before the last uppercase letter of the sequence.
    s = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', s)
    # Insert underscore before any uppercase letter that is not preceded by an underscore
    s = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s)
    return s.lower()

def to_camel(s: str) -> str:
    if not isinstance(s, str):
        raise TypeError("Input must be a string.")
    if not s:
        return ""

    parts = s.split('_')
    if not parts:
        return ""

    # Lowercase the first part
    camel_case_parts = [parts[0].lower()]

    # Capitalize the first letter of subsequent parts
    for part in parts[1:]:
        if part: # Ensure part is not empty
            camel_case_parts.append(part[0].upper() + part[1:].lower())
        else:
            # Handle cases with consecutive underscores, e.g., "my__var"
            # An empty part should not introduce an uppercase letter
            pass 
            
    return "".join(camel_case_parts)
