import re
from typing import List, Tuple


def parse_accept_language(value: str) -> List[Tuple[str, float]]:
    """
    Parse an HTTP Accept-Language header into a list of (language_tag, quality) pairs
    sorted by quality descending, with ties kept in original left-to-right order.
    
    Args:
        value: The Accept-Language header value string
        
    Returns:
        List of (language_tag, quality) tuples sorted by quality descending
        
    Raises:
        ValueError: If the header is malformed
    """
    # Handle empty or whitespace-only input
    if not value or not value.strip():
        return []
    
    # Split on comma
    entries = value.split(',')
    
    result = []
    
    for entry in entries:
        entry = entry.strip()
        
        # Skip empty entries
        if not entry:
            continue
        
        # Split on semicolon
        parts = entry.split(';')
        
        # Check for more than one semicolon
        if len(parts) > 2:
            raise ValueError("Entry contains more than one semicolon")
        
        # Extract language tag
        lang_tag = parts[0].strip()
        
        # Check for empty language tag
        if not lang_tag:
            raise ValueError("Empty language tag")
        
        # Lowercase the language tag (except wildcard)
        lang_tag = lang_tag.lower()
        
        # Default quality is 1.0
        quality = 1.0
        
        # Parse q-parameter if present
        if len(parts) == 2:
            q_param = parts[1].strip()
            
            # Parse the q-parameter
            if '=' not in q_param:
                raise ValueError("Malformed q-parameter: missing '='")
            
            q_parts = q_param.split('=')
            if len(q_parts) != 2:
                raise ValueError("Malformed q-parameter: multiple '=' signs")
            
            q_key = q_parts[0].strip()
            q_value = q_parts[1].strip()
            
            # Check q-parameter key (case-insensitive)
            if q_key.lower() != 'q':
                raise ValueError(f"Unknown parameter: {q_key}")
            
            # Validate and parse q-value
            if not q_value:
                raise ValueError("Empty q-value")
            
            # Check if q_value is a valid number with at most 3 decimal places
            # Valid formats: 0, 1, 0.8, 0.001, etc.
            if not re.match(r'^(0|1)(\.\d{1,3})?$', q_value):
                raise ValueError(f"Invalid q-value: {q_value}")
            
            try:
                quality = float(q_value)
            except ValueError:
                raise ValueError(f"Invalid q-value: {q_value}")
            
            # Check range [0, 1]
            if quality < 0.0 or quality > 1.0:
                raise ValueError(f"q-value out of range: {quality}")
        
        # Skip entries with q=0
        if quality == 0.0:
            continue
        
        result.append((lang_tag, quality))
    
    # Sort by quality descending (stable sort preserves original order for ties)
    result.sort(key=lambda x: x[1], reverse=True)
    
    return result
