import re

def parse_duration(text: str) -> int:
    if not text:
        raise ValueError("Input cannot be empty")

    # Define the conversion factors for each unit
    unit_to_seconds = {
        'w': 604800,  # week
        'd': 86400,   # day
        'h': 3600,    # hour
        'm': 60,      # minute
        's': 1        # second
    }

    # Regular expression to match the pattern of the duration string
    pattern = re.compile(r'(\d+)([wdhms])')
    matches = pattern.findall(text)

    # Check if the entire string was matched
    if not matches or ''.join(f"{num}{unit}" for num, unit in matches) != text:
        raise ValueError("Invalid duration string format")

    total_seconds = 0

    for number, unit in matches:
        if unit not in unit_to_seconds:
            raise ValueError(f"Unknown unit: {unit}")
        total_seconds += int(number) * unit_to_seconds[unit]

    return total_seconds
