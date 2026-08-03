def parse_email_headers(raw):
    """
    Parse RFC 5322-style email headers into a dictionary.
    
    Args:
        raw: String containing email headers
        
    Returns:
        Dictionary with Title-Case header names as keys and unfolded values
    """
    if not raw:
        return {}
    
    lines = raw.split('\n')
    headers = {}
    current_header = None
    current_value = None
    
    for line in lines:
        # Check for blank line (header/body separator)
        if line == '':
            break
            
        # Check if this is a continuation line (starts with whitespace)
        if line and (line[0] == ' ' or line[0] == '\t'):
            if current_header is not None:
                # Append to current value with a space separator
                current_value += ' ' + line.strip()
        else:
            # Save previous header if exists
            if current_header is not None:
                headers[current_header] = current_value
            
            # Parse new header
            if ':' in line:
                header_name, header_value = line.split(':', 1)
                # Normalize to Title-Case
                current_header = header_name.strip().title()
                # Replace underscores and hyphens properly for Title-Case
                # Split by hyphen, title-case each part, rejoin
                parts = current_header.split('-')
                current_header = '-'.join(part.capitalize() for part in parts)
                current_value = header_value.strip()
            else:
                # Invalid header line, skip
                current_header = None
                current_value = None
    
    # Don't forget the last header
    if current_header is not None:
        headers[current_header] = current_value
    
    return headers
