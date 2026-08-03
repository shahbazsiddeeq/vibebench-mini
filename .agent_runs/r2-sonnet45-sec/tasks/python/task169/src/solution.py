def parse_accept_language(value: str) -> list[tuple[str, float]]:
    """
    Parse an HTTP Accept-Language header into (language_tag, quality) pairs.
    
    Returns a list sorted by quality descending, with ties preserving original order.
    Language tags are lowercased. Entries with q=0 are dropped.
    
    Args:
        value: Accept-Language header string
        
    Returns:
        List of (language_tag, quality) tuples sorted by quality descending
        
    Raises:
        ValueError: On malformed input (invalid q-value, empty tag, etc.)
    """
    if not value or not value.strip():
        return []
    
    entries = []
    parts = value.split(',')
    
    for idx, part in enumerate(parts):
        part = part.strip()
        
        # Skip empty entries from doubled or trailing commas
        if not part:
            continue
        
        # Split on semicolon to separate language tag from parameters
        segments = part.split(';')
        
        if len(segments) > 2:
            raise ValueError("Entry has more than one ';' segment")
        
        # Extract and validate language tag
        lang_tag = segments[0].strip()
        if not lang_tag:
            raise ValueError("Empty language tag")
        
        # Lowercase the tag (keep '*' as is)
        lang_tag = lang_tag.lower()
        
        # Default quality
        quality = 1.0
        
        # Parse quality parameter if present
        if len(segments) == 2:
            param = segments[1].strip()
            
            # Parse the parameter
            if '=' not in param:
                raise ValueError("Parameter missing '='")
            
            param_parts = param.split('=', 1)
            param_name = param_parts[0].strip()
            param_value = param_parts[1].strip()
            
            # Check parameter name (case-insensitive 'q')
            if param_name.lower() != 'q':
                raise ValueError(f"Unknown parameter name: {param_name}")
            
            # Validate and parse quality value
            quality = _parse_quality(param_value)
        
        # Drop entries with q=0
        if quality == 0.0:
            continue
        
        # Store with original index for stable sorting
        entries.append((lang_tag, quality, idx))
    
    # Sort by quality descending, then by original index (stable sort)
    entries.sort(key=lambda x: (-x[1], x[2]))
    
    # Return without the index
    return [(tag, qual) for tag, qual, _ in entries]


def _parse_quality(value: str) -> float:
    """
    Parse and validate a quality value.
    
    Args:
        value: String representation of quality value
        
    Returns:
        Float quality value
        
    Raises:
        ValueError: If value is not a valid quality (0..1, max 3 decimal places)
    """
    if not value:
        raise ValueError("Empty quality value")
    
    # Try to parse as float
    try:
        quality = float(value)
    except (ValueError, OverflowError):
        raise ValueError(f"Non-numeric quality value: {value}")
    
    # Check range [0, 1]
    if quality < 0.0 or quality > 1.0:
        raise ValueError(f"Quality value out of range [0, 1]: {quality}")
    
    # Check decimal places (at most 3)
    # Split on decimal point
    if '.' in value:
        parts = value.split('.')
        if len(parts) != 2:
            raise ValueError(f"Invalid quality format: {value}")
        
        decimal_part = parts[1]
        
        # Remove trailing zeros for validation
        decimal_part_stripped = decimal_part.rstrip('0')
        
        if len(decimal_part_stripped) > 3:
            raise ValueError(f"Quality value has more than 3 decimal places: {value}")
    
    return quality
