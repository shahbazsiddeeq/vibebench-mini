import re

def parse_duration(text: str) -> int:
    """
    Convert a compact duration string into total number of seconds.
    
    The string consists of one or more segments, each being a non-negative integer
    followed by a single lowercase unit character:
    - 'w' = 604800s (week)
    - 'd' = 86400s (day)
    - 'h' = 3600s (hour)
    - 'm' = 60s (minute)
    - 's' = 1s (second)
    
    Args:
        text: A duration string matching the grammar
        
    Returns:
        Total number of seconds as an integer
        
    Raises:
        ValueError: If the input doesn't match the grammar
    """
    # Define unit conversions
    units = {
        'w': 604800,
        'd': 86400,
        'h': 3600,
        'm': 60,
        's': 1
    }
    
    # Pattern: one or more segments of (digits followed by a single lowercase unit letter)
    # Using fullmatch to ensure the entire string matches (no partial matches)
    pattern = r'^(\d+[wdhms])+$'
    
    if not re.fullmatch(pattern, text):
        raise ValueError(f"Invalid duration string: {text}")
    
    # Parse segments and sum up the seconds
    total_seconds = 0
    segment_pattern = r'(\d+)([wdhms])'
    
    for match in re.finditer(segment_pattern, text):
        number = int(match.group(1))
        unit = match.group(2)
        total_seconds += number * units[unit]
    
    return total_seconds
