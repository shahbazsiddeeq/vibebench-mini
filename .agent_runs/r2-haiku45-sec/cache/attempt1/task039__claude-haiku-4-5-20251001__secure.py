"""Run-Length Encoding module with security-conscious implementation."""

import re
from typing import Union


def rle_encode(s: str) -> str:
    """
    Encode a string using run-length encoding.
    
    Consecutive runs of characters are encoded as count+char.
    Example: "aaabbc" -> "3a2b1c"
    
    Args:
        s: Input string to encode. Must not contain ASCII digits (0-9).
        
    Returns:
        Encoded string with format: count+char repeated for each run.
        
    Raises:
        ValueError: If input contains any ASCII digit (0-9).
        TypeError: If input is not a string.
    """
    if not isinstance(s, str):
        raise TypeError("Input must be a string")
    
    # Check for digits in input
    if any(c.isdigit() for c in s):
        raise ValueError("Input must not contain ASCII digits (0-9)")
    
    # Handle empty string
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
        
        # Append count and character to result
        result.append(str(count) + current_char)
        i += count
    
    return "".join(result)


def rle_decode(s: str) -> str:
    """
    Decode a run-length encoded string.
    
    Reverses the encoding process. Input must be a concatenation of tokens,
    each consisting of one or more digits (count, must be non-zero) followed
    by exactly one non-digit character.
    Example: "3a2b1c" -> "aaabbc"
    
    Args:
        s: Encoded string to decode.
        
    Returns:
        Decoded string.
        
    Raises:
        ValueError: If input is malformed (invalid token structure or zero count).
        TypeError: If input is not a string.
    """
    if not isinstance(s, str):
        raise TypeError("Input must be a string")
    
    # Handle empty string
    if not s:
        return ""
    
    # Pattern: one or more digits followed by exactly one non-digit character
    # This pattern must match the entire string when concatenated
    pattern = r'^(\d+[^\d])*$'
    
    if not re.match(pattern, s):
        raise ValueError("Malformed input: invalid token structure")
    
    result = []
    i = 0
    
    while i < len(s):
        # Extract digits (count)
        count_str = ""
        while i < len(s) and s[i].isdigit():
            count_str += s[i]
            i += 1
        
        # Check if we have a count
        if not count_str:
            raise ValueError("Malformed input: missing count")
        
        # Convert count to integer
        try:
            count = int(count_str)
        except ValueError:
            raise ValueError("Malformed input: invalid count")
        
        # Check for zero count
        if count == 0:
            raise ValueError("Malformed input: count must be non-zero")
        
        # Extract character (must be exactly one non-digit)
        if i >= len(s):
            raise ValueError("Malformed input: missing character after count")
        
        if s[i].isdigit():
            raise ValueError("Malformed input: character cannot be a digit")
        
        char = s[i]
        i += 1
        
        # Append repeated character to result
        result.append(char * count)
    
    return "".join(result)
