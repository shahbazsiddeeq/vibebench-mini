def find_replace(text, replacements):
    # Sort keys by length in descending order to prioritize longer keys
    sorted_keys = sorted(replacements.keys(), key=len, reverse=True)
    
    # Initialize the result and index
    result = []
    i = 0
    
    while i < len(text):
        # Try to match any of the keys at the current position
        match_found = False
        for key in sorted_keys:
            if text.startswith(key, i):
                # If a match is found, append the replacement and move the index
                result.append(replacements[key])
                i += len(key)
                match_found = True
                break
        if not match_found:
            # If no match is found, append the current character and move the index
            result.append(text[i])
            i += 1
    
    return ''.join(result)
