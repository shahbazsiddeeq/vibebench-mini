def rle_encode(s: str) -> str:
    """
    Encode a string using run-length encoding.
    
    Args:
        s: Input string to encode. Must not contain ASCII digits (0-9).
        
    Returns:
        Run-length encoded string where consecutive runs are represented as count+char.
        
    Raises:
        ValueError: If input contains any ASCII digit (0-9).
    """
    if not isinstance(s, str):
        raise ValueError("Input must be a string")
    
    # Check for digits in input
    for char in s:
        if char.isdigit():
            raise ValueError("Input must not contain ASCII digits (0-9)")
    
    if not s:
        return ""
    
    result = []
    i = 0
    
    while i < len(s):
        current_char = s[i]
        count = 1
        
        # Count consecutive occurrences of the same character
        while i + count < len(s) and s[i + count] == current_char:
            count += 1
        
        result.append(f"{count}{current_char}")
        i += count
    
    return "".join(result)


def rle_decode(s: str) -> str:
    """
    Decode a run-length encoded string.
    
    Args:
        s: Run-length encoded string. Must be a concatenation of tokens,
           each consisting of one or more digits (non-zero count) followed
           by exactly one non-digit character.
           
    Returns:
        Decoded string.
        
    Raises:
        ValueError: If input is malformed (invalid format or zero count).
    """
    if not isinstance(s, str):
        raise ValueError("Input must be a string")
    
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
        
        # Must have at least one character after the count
        if i >= len(s):
            raise ValueError("Expected character after count")
        
        count = int(count_str)
        
        # Count must be non-zero
        if count == 0:
            raise ValueError("Count must be non-zero")
        
        # Get the character to repeat
        char = s[i]
        i += 1
        
        # Append the repeated character
        result.append(char * count)
    
    return "".join(result)
