import collections

def parse_email_headers(raw: str) -> dict:
    """
    Parses RFC 5322-style headers "Key: value" into a dictionary.

    Args:
        raw: A string containing the raw email headers.

    Returns:
        A dictionary where keys are case-normalized header names (Title-Case)
        and values are the unfolded header values.
    """
    if not isinstance(raw, str):
        raise TypeError("Input 'raw' must be a string.")

    headers = collections.OrderedDict()
    lines = raw.splitlines()
    
    i = 0
    while i < len(lines):
        line = lines[i]

        # Stop at the first blank line (header/body separator)
        if not line.strip():
            break

        # Check for folded header line
        if line.startswith(' ') or line.startswith('\t'):
            if not headers:
                # Malformed: folded line without a preceding header.
                # We'll skip this line as per robust parsing, or raise an error.
                # For this task, we'll just ignore it as it can't be attached.
                i += 1
                continue
            
            # This is a continuation of the previous header's value
            # Get the last added header name to append to its value
            last_header_name = next(reversed(headers))
            
            # Append the stripped continuation line part, joined by a single space
            # The previous value might already have leading/trailing whitespace from its own line
            # We strip the current line part and then join.
            # The problem statement says "leading/trailing whitespace on each part is stripped"
            # and "joins the parts with a single space".
            # This implies that if a part is " value ", it becomes "value".
            # If the previous value was "Hello" and current is " world", it becomes "Hello world".
            # If previous was "Hello " and current is " world", it becomes "Hello world".
            # So, we strip the current line and append. The previous value should also be stripped
            # before appending, but since we're building it incrementally, we ensure each part
            # is stripped before joining.
            
            current_value = headers[last_header_name]
            # If the current_value already has a space at the end from a previous fold,
            # or if the new part starts with a space, we need to be careful not to
            # add extra spaces. The simplest way is to strip both and join with one space.
            headers[last_header_name] = f"{current_value.strip()} {line.strip()}"
        else:
            # New header line
            parts = line.split(':', 1)
            if len(parts) == 2:
                name = parts[0].strip()
                value = parts[1].strip()

                # Normalize header name to Title-Case
                # This is a common normalization, but RFC 5322 doesn't strictly define
                # "Title-Case" for header names. It's usually "Capital-Hyphenated-Words".
                # The example "content-type" -> "Content-Type" suggests this.
                normalized_name_parts = [p.capitalize() for p in name.split('-')]
                normalized_name = '-'.join(normalized_name_parts)
                
                headers[normalized_name] = value
            else:
                # Malformed header line (no colon or empty key/value after strip)
                # We'll ignore malformed lines as per robust parsing.
                pass
        i += 1
    
    return dict(headers)
