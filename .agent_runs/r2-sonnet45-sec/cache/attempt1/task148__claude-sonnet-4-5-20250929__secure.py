import re


def parse_duration(text: str) -> int:
    """
    Parse a compact duration string into total seconds.
    
    Args:
        text: A string of one or more segments, each consisting of a non-negative
              integer followed by a unit character (w/d/h/m/s).
    
    Returns:
        Total number of seconds as an integer.
    
    Raises:
        ValueError: If the input doesn't match the expected format.
    """
    # Validate input type
    if not isinstance(text, str):
        raise ValueError("Input must be a string")
    
    # Check for empty string
    if not text:
        raise ValueError("Empty string is not a valid duration")
    
    # Define unit multipliers (seconds per unit)
    units = {
        'w': 604800,  # week
        'd': 86400,   # day
        'h': 3600,    # hour
        'm': 60,      # minute
        's': 1        # second
    }
    
    # Pattern: one or more segments of (digits)(unit)
    # Use fullmatch to ensure the entire string matches (no trailing junk)
    pattern = r'^(\d+[wdhms])+$'
    
    if not re.fullmatch(pattern, text):
        raise ValueError(f"Invalid duration format: {text}")
    
    # Extract all segments (number + unit pairs)
    segment_pattern = r'(\d+)([wdhms])'
    matches = re.findall(segment_pattern, text)
    
    # Calculate total seconds
    total_seconds = 0
    for number_str, unit in matches:
        # Convert number string to integer
        number = int(number_str)
        # Add to total
        total_seconds += number * units[unit]
    
    return total_seconds
