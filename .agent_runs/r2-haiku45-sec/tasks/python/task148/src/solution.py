import re

def parse_duration(text: str) -> int:
    """
    Convert a compact duration string into total seconds.
    
    The string consists of one or more segments, each being a non-negative integer
    followed by a single lowercase unit character:
    - 'w' = 604800 seconds (week)
    - 'd' = 86400 seconds (day)
    - 'h' = 3600 seconds (hour)
    - 'm' = 60 seconds (minute)
    - 's' = 1 second
    
    Args:
        text: A duration string matching the grammar
        
    Returns:
        Total duration in seconds
        
    Raises:
        ValueError: If the input doesn't match the grammar exactly
    """
    # Validate input type
    if not isinstance(text, str):
        raise ValueError("Input must be a string")
    
    # Empty string is invalid
    if not text:
        raise ValueError("Duration string cannot be empty")
    
    # Define unit conversions
    unit_to_seconds = {
        'w': 604800,
        'd': 86400,
        'h': 3600,
        'm': 60,
        's': 1,
    }
    
    # Pattern: one or more segments of (digits followed by a single lowercase unit)
    # Using fullmatch to ensure the entire string matches (no partial matches)
    pattern = r'^(\d+[wdhms])+$'
    
    if not re.fullmatch(pattern, text):
        raise ValueError(f"Invalid duration format: {text}")
    
    # Parse segments and sum up seconds
    total_seconds = 0
    
    # Extract all segments: number + unit pairs
    segment_pattern = r'(\d+)([wdhms])'
    matches = re.findall(segment_pattern, text)
    
    for number_str, unit in matches:
        number = int(number_str)
        total_seconds += number * unit_to_seconds[unit]
    
    return total_seconds
