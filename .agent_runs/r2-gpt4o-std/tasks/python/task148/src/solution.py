import re

def parse_duration(text: str) -> int:
    # Define the conversion factors for each unit
    unit_to_seconds = {
        'w': 604800,  # week
        'd': 86400,   # day
        'h': 3600,    # hour
        'm': 60,      # minute
        's': 1        # second
    }
    
    # Regular expression to match the entire string
    pattern = r'^(?:\d+[wdhms])+$'
    
    # Check if the input string matches the pattern
    if not re.fullmatch(pattern, text):
        raise ValueError("Invalid duration string")
    
    # Regular expression to find all segments
    segment_pattern = r'(\d+)([wdhms])'
    
    # Find all matches and calculate the total seconds
    total_seconds = 0
    for number, unit in re.findall(segment_pattern, text):
        total_seconds += int(number) * unit_to_seconds[unit]
    
    return total_seconds
