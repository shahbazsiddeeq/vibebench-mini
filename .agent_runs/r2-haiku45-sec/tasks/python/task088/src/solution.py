"""
Email Header Parser - RFC 5322 style header parsing.
"""

import re
from typing import Dict


def parse_email_headers(raw: str) -> Dict[str, str]:
    """
    Parse RFC 5322-style email headers into a dictionary.
    
    Rules:
    - Header names are case-normalized to Title-Case
    - Folded headers (continuation lines starting with whitespace) are unfolded
    - Parsing stops at the first blank line
    - For duplicate headers, the last occurrence wins
    
    Args:
        raw: Raw email header string
        
    Returns:
        Dictionary mapping header names to their values
    """
    if not raw:
        return {}
    
    headers: Dict[str, str] = {}
    lines = raw.split('\n')
    
    current_header_name: str = ""
    current_header_value: str = ""
    
    for line in lines:
        # Check for blank line (end of headers)
        if line.strip() == "":
            # Save the last header if any
            if current_header_name:
                headers[current_header_name] = current_header_value
            break
        
        # Check if this is a continuation line (starts with space or tab)
        if line and line[0] in (' ', '\t'):
            # This is a folded continuation line
            if current_header_name:
                # Append to current header value with a space separator
                current_header_value += " " + line.strip()
        else:
            # This is a new header line
            # First, save the previous header if any
            if current_header_name:
                headers[current_header_name] = current_header_value
            
            # Parse the new header
            colon_index = line.find(':')
            if colon_index == -1:
                # Invalid header line without colon, skip it
                current_header_name = ""
                current_header_value = ""
                continue
            
            header_name = line[:colon_index].strip()
            header_value = line[colon_index + 1:].strip()
            
            # Normalize header name to Title-Case
            current_header_name = normalize_header_name(header_name)
            current_header_value = header_value
    
    # Don't forget to save the last header if we didn't hit a blank line
    if current_header_name:
        headers[current_header_name] = current_header_value
    
    return headers


def normalize_header_name(name: str) -> str:
    """
    Normalize header name to Title-Case format.
    
    Examples:
        "content-type" -> "Content-Type"
        "from" -> "From"
        "x-custom-header" -> "X-Custom-Header"
    
    Args:
        name: The header name to normalize
        
    Returns:
        Title-cased header name
    """
    # Split by hyphens and capitalize each part
    parts = name.split('-')
    normalized_parts = [part.capitalize() for part in parts]
    return '-'.join(normalized_parts)
