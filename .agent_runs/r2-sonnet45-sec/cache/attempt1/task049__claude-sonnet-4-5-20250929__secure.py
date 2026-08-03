def find_replace(text: str, replacements: dict) -> str:
    """
    Apply all replacements simultaneously to the text.
    Longer keys take priority over shorter overlapping keys.
    
    Args:
        text: The input text to process
        replacements: Dictionary mapping search strings to replacement strings
    
    Returns:
        The text with all replacements applied simultaneously
    """
    if not text or not replacements:
        return text
    
    # Validate inputs
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if not isinstance(replacements, dict):
        raise TypeError("replacements must be a dictionary")
    
    # Validate all keys and values are strings
    for key, value in replacements.items():
        if not isinstance(key, str):
            raise TypeError("All replacement keys must be strings")
        if not isinstance(value, str):
            raise TypeError("All replacement values must be strings")
        if not key:  # Empty keys are not allowed
            raise ValueError("Replacement keys cannot be empty strings")
    
    # Sort keys by length (descending) to prioritize longer matches
    sorted_keys = sorted(replacements.keys(), key=len, reverse=True)
    
    # Track which positions have been replaced
    replaced_positions = set()
    
    # Store replacements as (start_pos, end_pos, replacement_text)
    pending_replacements = []
    
    # Find all matches, prioritizing longer keys
    for key in sorted_keys:
        key_len = len(key)
        pos = 0
        
        while pos <= len(text) - key_len:
            # Check if we found the key at this position
            if text[pos:pos + key_len] == key:
                # Check if any position in this range has already been replaced
                if not any(p in replaced_positions for p in range(pos, pos + key_len)):
                    # Mark these positions as replaced
                    for p in range(pos, pos + key_len):
                        replaced_positions.add(p)
                    
                    # Store the replacement
                    pending_replacements.append((pos, pos + key_len, replacements[key]))
                    
                    # Move past this match
                    pos += key_len
                else:
                    # Skip this overlapping match
                    pos += 1
            else:
                pos += 1
    
    # Sort replacements by position to build result in order
    pending_replacements.sort(key=lambda x: x[0])
    
    # Build the result string
    result = []
    last_pos = 0
    
    for start, end, replacement in pending_replacements:
        # Add text before this replacement
        result.append(text[last_pos:start])
        # Add the replacement
        result.append(replacement)
        last_pos = end
    
    # Add any remaining text
    result.append(text[last_pos:])
    
    return ''.join(result)
