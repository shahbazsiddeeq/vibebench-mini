# src/solution.py

def find_replace(text: str, replacements: dict) -> str:
    # Validate inputs
    if not isinstance(text, str):
        raise ValueError("text must be a string")
    if not isinstance(replacements, dict):
        raise ValueError("replacements must be a dictionary")
    
    # Sanitize keys and values in replacements
    sanitized_replacements = {}
    for key, value in replacements.items():
        if not isinstance(key, str) or not isinstance(value, str):
            raise ValueError("Both keys and values in replacements must be strings")
        sanitized_replacements[key] = value

    # Sort keys by length (longer keys first) to ensure priority
    sorted_keys = sorted(sanitized_replacements.keys(), key=len, reverse=True)

    # Create a copy of the original text to apply replacements
    result = text
    for key in sorted_keys:
        result = result.replace(key, sanitized_replacements[key])

    return result
