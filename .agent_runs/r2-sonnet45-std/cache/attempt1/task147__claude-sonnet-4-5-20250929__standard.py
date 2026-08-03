def parse_csv_line(line: str, delimiter: str = ',') -> list[str]:
    """
    Parse a single CSV line according to RFC4180 rules.
    
    Args:
        line: The CSV line to parse
        delimiter: Single character delimiter (cannot be '"')
    
    Returns:
        List of field values
        
    Raises:
        ValueError: If delimiter is invalid, quoted field is unterminated,
                   or there's text after a closing quote
    """
    # Validate delimiter
    if len(delimiter) != 1 or delimiter == '"':
        raise ValueError("Delimiter must be a single character other than '\"'")
    
    fields = []
    i = 0
    n = len(line)
    
    while i <= n:
        # Start of a new field
        field_start = i
        
        # Check if this field is quoted
        if i < n and line[i] == '"':
            # Quoted field
            i += 1  # Skip opening quote
            field_chars = []
            
            while i < n:
                if line[i] == '"':
                    # Check if it's an escaped quote or closing quote
                    if i + 1 < n and line[i + 1] == '"':
                        # Escaped quote: ""
                        field_chars.append('"')
                        i += 2
                    else:
                        # Closing quote
                        i += 1
                        # After closing quote, must be delimiter or end of line
                        if i < n and line[i] != delimiter:
                            raise ValueError("Text found after closing quote")
                        break
                else:
                    field_chars.append(line[i])
                    i += 1
            else:
                # Reached end of line without finding closing quote
                raise ValueError("Unterminated quoted field")
            
            fields.append(''.join(field_chars))
            
            # Move past the delimiter if present
            if i < n and line[i] == delimiter:
                i += 1
            # If we're at end of line, we're done with this field
            
        else:
            # Unquoted field - read until delimiter or end of line
            field_chars = []
            while i < n and line[i] != delimiter:
                field_chars.append(line[i])
                i += 1
            
            fields.append(''.join(field_chars))
            
            # Move past the delimiter if present
            if i < n and line[i] == delimiter:
                i += 1
        
        # If we've consumed the entire line, we're done
        if i > n:
            break
        # If we're exactly at the end and just passed a delimiter, add empty field
        if i == n and field_start < n and (field_start == 0 or line[field_start - 1] == delimiter):
            # We just processed a delimiter at the end
            if field_start > 0 and line[field_start - 1] == delimiter:
                fields.append('')
            break
    
    return fields
