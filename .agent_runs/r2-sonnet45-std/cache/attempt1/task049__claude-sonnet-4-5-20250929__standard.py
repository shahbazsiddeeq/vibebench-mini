def find_replace(text, replacements):
    if not replacements or not text:
        return text
    
    # Sort keys by length (descending) to prioritize longer matches
    sorted_keys = sorted(replacements.keys(), key=len, reverse=True)
    
    # Track which positions in the text have been matched
    # matched[i] will store (end_pos, replacement_text) if position i starts a match
    matched = {}
    
    i = 0
    while i < len(text):
        # Check if this position already part of a match
        if i in matched:
            i = matched[i][0]
            continue
        
        # Try to find a match starting at position i
        found = False
        for key in sorted_keys:
            if text[i:i+len(key)] == key:
                # Mark all positions covered by this match
                matched[i] = (i + len(key), replacements[key])
                found = True
                break
        
        if found:
            i = matched[i][0]
        else:
            i += 1
    
    # Build result
    result = []
    i = 0
    while i < len(text):
        if i in matched:
            end_pos, replacement = matched[i]
            result.append(replacement)
            i = end_pos
        else:
            result.append(text[i])
            i += 1
    
    return ''.join(result)
