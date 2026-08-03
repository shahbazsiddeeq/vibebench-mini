import re

def parse_duration(text: str) -> int:
    """
    Parse a compact duration string into total seconds.
    
    Format: one or more segments of <digits><unit>
    Units: w (week=604800s), d (day=86400s), h (hour=3600s), m (minute=60s), s (second=1s)
    
    Args:
        text: Duration string (e.g., "1h30m", "2d")
        
    Returns:
        Total number of seconds as int
        
    Raises:
        ValueError: If input doesn't match the required format
    """
    if not text:
        raise ValueError("Empty string is not a valid duration")
    
    # Define unit multipliers
    units = {
        'w': 604800,  # week
        'd': 86400,   # day
        'h': 3600,    # hour
        'm': 60,      # minute
        's': 1        # second
    }
    
    # Pattern: one or more segments of (digits)(unit)
    # Use fullmatch to ensure entire string matches
    pattern = r'^(\d+[wdhms])+$'
    
    if not re.fullmatch(pattern, text):
        raise ValueError(f"Invalid duration format: {text}")
    
    # Extract all segments
    segment_pattern = r'(\d+)([wdhms])'
    matches = re.findall(segment_pattern, text)
    
    total_seconds = 0
    for number_str, unit in matches:
        number = int(number_str)
        total_seconds += number * units[unit]
    
    return total_seconds
