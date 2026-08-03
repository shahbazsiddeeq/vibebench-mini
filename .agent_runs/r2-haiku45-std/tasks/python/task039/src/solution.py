def rle_encode(s: str) -> str:
    """
    Encodes a string using run-length encoding.
    Consecutive runs of characters are encoded as count+char.
    
    Args:
        s: Input string (must not contain ASCII digits 0-9)
        
    Returns:
        Encoded string
        
    Raises:
        ValueError: If input contains any ASCII digit
    """
    # Check for digits in input
    if any(c.isdigit() for c in s):
        raise ValueError("Input must not contain ASCII digits")
    
    if not s:
        return ""
    
    result = []
    i = 0
    while i < len(s):
        char = s[i]
        count = 1
        
        # Count consecutive occurrences of the same character
        while i + count < len(s) and s[i + count] == char:
            count += 1
        
        result.append(str(count) + char)
        i += count
    
    return "".join(result)


def rle_decode(s: str) -> str:
    """
    Decodes a run-length encoded string.
    
    Args:
        s: Encoded string (format: digits followed by a non-digit character, repeated)
        
    Returns:
        Decoded string
        
    Raises:
        ValueError: If input is malformed
    """
    if not s:
        return ""
    
    result = []
    i = 0
    
    while i < len(s):
        # Parse the count (one or more digits)
        if not s[i].isdigit():
            raise ValueError("Expected digit at position {}".format(i))
        
        count_str = ""
        while i < len(s) and s[i].isdigit():
            count_str += s[i]
            i += 1
        
        # Convert count to integer
        count = int(count_str)
        
        # Check for zero count
        if count == 0:
            raise ValueError("Count must be non-zero")
        
        # Parse the character (must be exactly one non-digit)
        if i >= len(s):
            raise ValueError("Expected character after count")
        
        if s[i].isdigit():
            raise ValueError("Expected non-digit character after count")
        
        char = s[i]
        i += 1
        
        result.append(char * count)
    
    return "".join(result)
