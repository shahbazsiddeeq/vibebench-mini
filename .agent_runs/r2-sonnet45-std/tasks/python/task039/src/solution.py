def rle_encode(s):
    """
    Encodes consecutive runs of characters as count+char.
    Raises ValueError if input contains ASCII digits (0-9).
    """
    if not s:
        return ""
    
    # Check for digits in input
    for char in s:
        if char.isdigit():
            raise ValueError("Input must not contain ASCII digits")
    
    result = []
    i = 0
    while i < len(s):
        current_char = s[i]
        count = 1
        
        # Count consecutive occurrences
        while i + count < len(s) and s[i + count] == current_char:
            count += 1
        
        result.append(str(count) + current_char)
        i += count
    
    return "".join(result)


def rle_decode(s):
    """
    Decodes run-length encoded strings.
    Valid format: one or more digits (non-zero count) followed by exactly one non-digit character.
    Raises ValueError for malformed input.
    """
    if not s:
        return ""
    
    result = []
    i = 0
    
    while i < len(s):
        # Parse the count (one or more digits)
        if not s[i].isdigit():
            raise ValueError("Expected digit at start of token")
        
        count_str = ""
        while i < len(s) and s[i].isdigit():
            count_str += s[i]
            i += 1
        
        # Check if we have a character after the count
        if i >= len(s):
            raise ValueError("Expected character after count")
        
        count = int(count_str)
        
        # Check for zero count
        if count == 0:
            raise ValueError("Count must be non-zero")
        
        # Get the character to repeat
        char = s[i]
        i += 1
        
        # Add repeated character to result
        result.append(char * count)
    
    return "".join(result)
