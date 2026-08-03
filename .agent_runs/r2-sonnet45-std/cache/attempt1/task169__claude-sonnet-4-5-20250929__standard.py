def parse_accept_language(value: str) -> list[tuple[str, float]]:
    """
    Parse an HTTP Accept-Language header into a list of (language_tag, quality) pairs.
    
    Args:
        value: The Accept-Language header value
        
    Returns:
        List of (language_tag, quality) tuples sorted by quality descending (stable)
    """
    if not value or not value.strip():
        return []
    
    entries = []
    
    # Split on comma
    parts = value.split(',')
    
    for part in parts:
        part = part.strip()
        
        # Skip empty entries
        if not part:
            continue
        
        # Split on semicolon to separate language tag from parameters
        segments = part.split(';')
        
        if len(segments) > 2:
            raise ValueError("More than one ';' segment")
        
        # Extract language tag
        lang_tag = segments[0].strip()
        
        if not lang_tag:
            raise ValueError("Empty language tag")
        
        # Lowercase the language tag (but keep '*' as is)
        lang_tag = lang_tag.lower()
        
        # Default quality
        quality = 1.0
        
        # Parse quality parameter if present
        if len(segments) == 2:
            param = segments[1].strip()
            
            # Parse q-parameter
            if '=' not in param:
                raise ValueError("Malformed parameter")
            
            key, val = param.split('=', 1)
            key = key.strip()
            val = val.strip()
            
            # Check if it's a q parameter (case-insensitive)
            if key.lower() != 'q':
                raise ValueError("Unknown parameter name")
            
            # Parse quality value
            try:
                quality = float(val)
            except ValueError:
                raise ValueError("Non-numeric q value")
            
            # Validate quality range
            if quality < 0 or quality > 1:
                raise ValueError("Quality out of range")
            
            # Validate at most 3 decimal places
            # Check by converting to string and examining decimal places
            val_str = val.strip()
            if '.' in val_str:
                decimal_part = val_str.split('.')[1]
                if len(decimal_part) > 3:
                    raise ValueError("Too many decimal places")
        
        # Skip entries with q=0
        if quality == 0:
            continue
        
        entries.append((lang_tag, quality, len(entries)))  # Include original index for stable sort
    
    # Sort by quality descending, keeping original order for ties (stable sort)
    # Python's sort is stable, so we just need to sort by quality descending
    entries.sort(key=lambda x: -x[1])
    
    # Remove the index we added for tracking
    return [(tag, qual) for tag, qual, _ in entries]
