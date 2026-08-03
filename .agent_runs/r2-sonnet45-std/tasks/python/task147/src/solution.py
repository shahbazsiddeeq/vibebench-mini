def parse_csv_line(line: str, delimiter: str = ',') -> list[str]:
    """Parse a single CSV line according to RFC4180 rules.
    
    Args:
        line: The CSV line to parse
        delimiter: Single character delimiter (default ',')
        
    Returns:
        List of field values
        
    Raises:
        ValueError: If delimiter is invalid or line has malformed quotes
    """
    # Validate delimiter
    if len(delimiter) != 1 or delimiter == '"':
        raise ValueError("Delimiter must be a single character other than '\"'")
    
    fields = []
    i = 0
    n = len(line)
    
    while i <= n:
        # Start of a new field
        if i == n:
            # End of line - we're done
            break
            
        if line[i] == '"':
            # Quoted field
            i += 1  # Skip opening quote
            field_chars = []
            
            while i < n:
                if line[i] == '"':
                    # Check if it's an escaped quote or closing quote
                    if i + 1 < n and line[i + 1] == '"':
                        # Escaped quote - add one quote to field
                        field_chars.append('"')
                        i += 2
                    else:
                        # Closing quote
                        i += 1
                        # Next char must be delimiter or end of line
                        if i < n and line[i] != delimiter:
                            raise ValueError("Text after closing quote")
                        break
                else:
                    field_chars.append(line[i])
                    i += 1
            else:
                # Reached end of line without closing quote
                raise ValueError("Unterminated quoted field")
            
            fields.append(''.join(field_chars))
            
            # Move past delimiter if present
            if i < n and line[i] == delimiter:
                i += 1
        else:
            # Unquoted field
            field_chars = []
            while i < n and line[i] != delimiter:
                field_chars.append(line[i])
                i += 1
            
            fields.append(''.join(field_chars))
            
            # Move past delimiter if present
            if i < n and line[i] == delimiter:
                i += 1
    
    return fields
