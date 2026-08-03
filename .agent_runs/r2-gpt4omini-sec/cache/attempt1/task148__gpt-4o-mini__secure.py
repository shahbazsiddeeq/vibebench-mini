# src/solution.py

import re

def parse_duration(text: str) -> int:
    # Define the regex pattern for matching the duration string
    pattern = r'^(?:(\d+)([wdhms]))+$'
    
    # Validate the input string
    if not isinstance(text, str) or not text:
        raise ValueError("Input must be a non-empty string.")
    
    # Match the entire string against the pattern
    matches = re.fullmatch(pattern, text)
    if matches is None:
        raise ValueError("Invalid duration format.")
    
    # Define the mapping of units to seconds
    unit_to_seconds = {
        'w': 604800,  # weeks
        'd': 86400,   # days
        'h': 3600,    # hours
        'm': 60,      # minutes
        's': 1        # seconds
    }
    
    total_seconds = 0
    # Iterate through the matches to calculate total seconds
    for match in re.finditer(r'(\d+)([wdhms])', text):
        number, unit = match.groups()
        if unit not in unit_to_seconds:
            raise ValueError("Unknown unit: {}".format(unit))
        
        total_seconds += int(number) * unit_to_seconds[unit]
    
    return total_seconds
