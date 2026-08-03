def find_replace(text, replacements):
    """
    Apply all replacements simultaneously to text.
    Longer keys take priority over shorter overlapping keys.
    """
    if not replacements or not text:
        return text
    
    # Sort keys by length (descending) to prioritize longer matches
    sorted_keys = sorted(replacements.keys(), key=len, reverse=True)
    
    result = []
    i = 0
    
    while i < len(text):
        matched = False
        
        # Try to match the longest keys first
        for key in sorted_keys:
            if text[i:i+len(key)] == key:
                result.append(replacements[key])
                i += len(key)
                matched = True
                break
        
        # If no key matched, keep the character as is
        if not matched:
            result.append(text[i])
            i += 1
    
    return ''.join(result)
