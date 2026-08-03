# src/solution.py

def parse_duration(text: str) -> int:
    if not text:
        raise ValueError("Input cannot be empty")
    
    unit_mapping = {
        'w': 604800,
        'd': 86400,
        'h': 3600,
        'm': 60,
        's': 1
    }
    
    total_seconds = 0
    i = 0
    length = len(text)
    
    while i < length:
        # Read the number
        num_start = i
        while i < length and text[i].isdigit():
            i += 1
        
        if num_start == i:  # No digits found
            raise ValueError("Invalid format: number expected")
        
        number = int(text[num_start:i])
        
        # Read the unit
        if i >= length or text[i] not in unit_mapping:
            raise ValueError("Invalid format: unit expected")
        
        unit = text[i]
        total_seconds += number * unit_mapping[unit]
        i += 1  # Move past the unit character
    
    return total_seconds
