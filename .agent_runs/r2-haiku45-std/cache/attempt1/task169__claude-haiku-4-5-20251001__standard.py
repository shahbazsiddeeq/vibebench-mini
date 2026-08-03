def parse_accept_language(value: str) -> list[tuple[str, float]]:
    """
    Parse an HTTP Accept-Language header into a list of (language_tag, quality) pairs
    sorted by quality DESCENDING, with ties kept in their original left-to-right order.
    """
    # Handle empty or whitespace-only input
    if not value or not value.strip():
        return []
    
    # Split by comma and process each entry
    entries = value.split(',')
    result = []
    
    for entry in entries:
        entry = entry.strip()
        
        # Skip empty entries
        if not entry:
            continue
        
        # Split by semicolon to separate language tag from parameters
        parts = entry.split(';')
        
        # Language tag is the first part
        lang_tag = parts[0].strip()
        
        # Validate that language tag is not empty
        if not lang_tag:
            raise ValueError("Empty language tag")
        
        # Lowercase the language tag (but keep '*' as is)
        lang_tag = lang_tag.lower()
        
        # Default quality is 1.0
        quality = 1.0
        
        # Process parameters (everything after the first semicolon)
        if len(parts) > 1:
            # Check for more than one semicolon
            if len(parts) > 2:
                raise ValueError("More than one semicolon in entry")
            
            param = parts[1].strip()
            
            # Parse the q-parameter
            if '=' not in param:
                raise ValueError("Malformed q-parameter")
            
            param_parts = param.split('=', 1)
            param_name = param_parts[0].strip()
            param_value = param_parts[1].strip()
            
            # Check parameter name (case-insensitive)
            if param_name.lower() != 'q':
                raise ValueError(f"Unknown parameter name: {param_name}")
            
            # Parse quality value
            try:
                quality = float(param_value)
            except ValueError:
                raise ValueError(f"Invalid quality value: {param_value}")
            
            # Validate quality is in range [0, 1]
            if quality < 0 or quality > 1:
                raise ValueError(f"Quality out of range: {quality}")
            
            # Validate at most 3 digits after decimal point
            if '.' in param_value:
                decimal_part = param_value.split('.')[1]
                if len(decimal_part) > 3:
                    raise ValueError(f"Too many decimal places in quality: {param_value}")
        
        # Skip entries with q=0 (not acceptable)
        if quality == 0:
            continue
        
        result.append((lang_tag, quality))
    
    # Sort by quality descending (stable sort preserves original order for ties)
    result.sort(key=lambda x: x[1], reverse=True)
    
    return result
