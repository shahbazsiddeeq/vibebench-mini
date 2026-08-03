# src/solution.py

def find_replace(text, replacements):
    # Sort replacements by key length in descending order
    sorted_replacements = sorted(replacements.items(), key=lambda item: -len(item[0]))
    
    # Create a new string to hold the result
    result = text
    
    # Apply each replacement
    for old, new in sorted_replacements:
        result = result.replace(old, new)
    
    return result
