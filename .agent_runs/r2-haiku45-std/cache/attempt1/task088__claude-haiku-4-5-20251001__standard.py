def parse_email_headers(raw: str) -> dict:
    """
    Parse RFC 5322-style email headers into a dictionary.
    
    Rules:
    - Header names are case-normalized to Title-Case
    - Folded headers (continuation lines starting with whitespace) are unfolded
    - Parsing stops at the first blank line
    - For duplicate headers, the last occurrence wins
    """
    if not raw:
        return {}
    
    headers = {}
    lines = raw.split('\n')
    
    current_header = None
    current_value = None
    
    for line in lines:
        # Check for blank line (end of headers)
        if line.strip() == '':
            break
        
        # Check if this is a continuation line (starts with whitespace)
        if line and line[0] in (' ', '\t'):
            # This is a folded header continuation
            if current_header is not None:
                # Strip leading/trailing whitespace from the continuation
                current_value += ' ' + line.strip()
        else:
            # This is a new header line
            # First, save the previous header if it exists
            if current_header is not None:
                headers[current_header] = current_value
            
            # Parse the new header
            if ':' in line:
                header_name, header_value = line.split(':', 1)
                # Normalize header name to Title-Case
                current_header = '-'.join(word.capitalize() for word in header_name.split('-'))
                # Strip leading/trailing whitespace from value
                current_value = header_value.strip()
            else:
                # Invalid header line without colon, skip it
                current_header = None
                current_value = None
    
    # Don't forget to add the last header
    if current_header is not None:
        headers[current_header] = current_value
    
    return headers
