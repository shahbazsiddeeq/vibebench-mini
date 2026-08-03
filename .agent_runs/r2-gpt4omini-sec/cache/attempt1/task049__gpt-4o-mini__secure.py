# src/solution.py

def find_replace(text: str, replacements: dict) -> str:
    # Validate input types
    if not isinstance(text, str):
        raise ValueError("text must be a string")
    if not isinstance(replacements, dict):
        raise ValueError("replacements must be a dictionary")
    
    # Validate keys and values in replacements
    for key, value in replacements.items():
        if not isinstance(key, str) or not isinstance(value, str):
            raise ValueError("All keys and values in replacements must be strings")
    
    # Sort replacements by key length (longer keys first)
    sorted_replacements = sorted(replacements.items(), key=lambda item: -len(item[0]))
    
    # Create a new text with replacements applied
    for key, value in sorted_replacements:
        text = text.replace(key, value)
    
    return text
