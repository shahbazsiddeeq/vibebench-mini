def parse_email_headers(raw: str) -> dict:
    """
    Parse RFC 5322-style email headers into a dictionary.
    
    Args:
        raw: Raw email header string
        
    Returns:
        Dictionary mapping header names (Title-Case) to their values
    """
    if not isinstance(raw, str):
        raise TypeError("Input must be a string")
    
    headers = {}
    lines = raw.split('\n')
    
    current_header = None
    current_value = None
    
    for line in lines:
        # Stop at first blank line (header/body separator)
        if line == '':
            break
            
        # Check if this is a continuation line (starts with whitespace)
        if line and (line[0] == ' ' or line[0] == '\t'):
            # This is a folded header continuation
            if current_header is not None:
                # Strip leading/trailing whitespace and append with single space
                current_value += ' ' + line.strip()
            # If no current header, this is malformed but we'll ignore it
            continue
        
        # Check if this line contains a header (has a colon)
        if ':' in line:
            # Save previous header if exists
            if current_header is not None:
                headers[current_header] = current_value
            
            # Parse new header
            colon_pos = line.index(':')
            header_name = line[:colon_pos]
            header_value = line[colon_pos + 1:]
            
            # Normalize header name to Title-Case
            # Handle hyphenated headers properly
            current_header = '-'.join(word.capitalize() for word in header_name.split('-'))
            
            # Strip leading/trailing whitespace from value
            current_value = header_value.strip()
        else:
            # Line without colon and not a continuation - save current and reset
            if current_header is not None:
                headers[current_header] = current_value
                current_header = None
                current_value = None
    
    # Don't forget to save the last header if exists
    if current_header is not None:
        headers[current_header] = current_value
    
    return headers
