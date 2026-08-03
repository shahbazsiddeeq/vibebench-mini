# src/solution.py

def find_replace(text, replacements):
    if not isinstance(text, str) or not isinstance(replacements, dict):
        raise ValueError("Invalid input types.")

    # Sort replacements by key length in descending order
    sorted_replacements = sorted(replacements.items(), key=lambda x: -len(x[0]))

    # Initialize the result and index
    result = []
    i = 0

    while i < len(text):
        # Try to match any of the replacement keys
        match_found = False
        for key, value in sorted_replacements:
            if text.startswith(key, i):
                result.append(value)
                i += len(key)
                match_found = True
                break
        if not match_found:
            result.append(text[i])
            i += 1

    return ''.join(result)
